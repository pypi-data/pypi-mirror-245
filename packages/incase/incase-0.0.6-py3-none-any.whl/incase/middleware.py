import json

from starlette.middleware.base import BaseHTTPMiddleware

from incase import Case, Caseless


class MaybeJsonAsyncIterator:
    """This is used to wrap the iterable body of the streaming response
    so that the json keys can be handled when the iterable is called.
    """

    def __init__(self, base_iterable):
        self._async_iterable = base_iterable

    def __aiter__(self):
        return self

    async def __anext__(self):
        async for item in self._async_iterable:
            json_content = json.loads(item)
            return json.dumps(
                {
                    Caseless(key)[Case.CAMEL]: value
                    for key, value in json_content.items()
                }
            ).encode(encoding="utf-8")
        raise StopAsyncIteration


class JSONCaseTranslatorMiddleware(BaseHTTPMiddleware):
    """This middleware translates the case of json keys recieved and sent by the
    asgi app. It is helpful for allowing a python back-end to use snake_case
    while allowing a javascript front end to use camelCase."""

    async def dispatch(self, request, call_next):
        try:
            data = await request.body()
            request._body = json.dumps(
                {
                    Caseless(key)[Case.SNAKE]: value
                    for key, value in json.loads(data).items()
                }
            ).encode(encoding="utf-8")
        except json.JSONDecodeError:
            pass  # guess it wasn't json
        request.this = "hi"
        response = await call_next(request)
        if response.headers.get("content-type") == "application/json":
            response.body_iterator = MaybeJsonAsyncIterator(response.body_iterator)
        return response
