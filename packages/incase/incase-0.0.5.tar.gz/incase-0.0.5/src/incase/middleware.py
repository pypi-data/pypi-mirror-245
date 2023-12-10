import json

from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.datastructures import Headers, MutableHeaders
from incase import Caseless, Case


class JSONCaseTranslatorMiddleware:
    """This middleware translates the case of json keys recieved and sent by the
    asgi app. It is helpful for allowing a python back-end to use snake_case
    while allowing a javascript front end to use camelCase."""

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            responder = _CaseModifyingResponder(self.app)
            await responder(scope, receive, send)
            return
        await self.app(scope, receive, send)


class _CaseModifyingResponder:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.receive: Receive = unattached_receive
        self.send: Send = unattached_send
        self.accepts_json = False
        self.sent_json = False
        self.initial_message: Message = {}

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        headers = MutableHeaders(scope=scope)
        self.content_type_json = "application/json" in headers.get("content-type", "")
        self.receive = receive
        self.send = send
        await self.app(scope, self.receive_json, self.send_json)

    async def receive_json(self) -> Message:
        message = await self.receive()

        if not self.content_type_json:
            return message

        assert message["type"] == "http.request"

        body = message["body"]
        more_body = message.get("more_body", False)
        if more_body:
            # Some implementations (e.g. HTTPX) may send one more empty-body message.
            # Make sure they don't send one that contains a body, or it means
            # that clients attempt to stream the request body.
            message = await self.receive()
            if message["body"] != b"":  # pragma: no cover
                raise NotImplementedError(
                    "Streaming the request body isn't supported yet"
                )

        obj = {
            Caseless(key)[Case.SNAKE]: value for key, value in json.loads(body).items()
        }
        message["body"] = json.dumps(obj).encode()

        return message

    async def send_json(self, message: Message) -> None:
        if message["type"] == "http.response.start":
            headers = Headers(raw=message["headers"])
            if headers["content-type"] != "application/json":
                # Client accepts msgpack, but the app did not send JSON data.
                # (Note that it may have sent msgpack-encoded data.)
                self.should_encode_from_json_to_msgpack = False
                await self.send(message)
                return

            # Don't send the initial message until we've determined how to
            # modify the ougoging headers correctly.
            self.initial_message = message

        elif message["type"] == "http.response.body":
            body = message.get("body", b"")
            more_body = message.get("more_body", False)
            if more_body:  # pragma: no cover
                raise NotImplementedError(
                    "Streaming the response body isn't supported yet"
                )

            body = json.dumps(
                {
                    Caseless(key)[Case.CAMEL]: value
                    for key, value in json.loads(body).items()
                }
            ).encode("utf-8")

            headers = MutableHeaders(raw=self.initial_message["headers"])
            headers["Content-Type"] = "application/json"
            headers["Content-Length"] = str(len(body))
            message["body"] = body

            await self.send(self.initial_message)
            await self.send(message)


async def unattached_receive() -> Message:
    raise RuntimeError("receive awaitable not set")  # pragma: no cover


async def unattached_send(message: Message) -> None:
    raise RuntimeError("send awaitable not set")  # pragma: no cover
