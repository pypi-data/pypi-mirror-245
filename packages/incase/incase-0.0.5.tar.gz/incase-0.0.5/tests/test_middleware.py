from unittest import TestCase, main

from incase.middleware import JSONCaseTranslatorMiddleware
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

SNAKE_DATA = {"first_thing": 1, "second_thing": 2}


def generic_get(request):
    return JSONResponse(SNAKE_DATA)


async def greeting(request):
    data = await request.json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    message = {"hello": f"{first_name} {last_name}"}
    return JSONResponse(message)


routes = [
    Route("/", generic_get),
    Route("/greeting", endpoint=greeting, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)

app.add_middleware(JSONCaseTranslatorMiddleware)

client = TestClient(app)


class TestCaseTranslateMiddleware(TestCase):
    def test_get(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"firstThing": 1, "secondThing": 2})

    def test_post(self):
        response = client.post(
            "/greeting", json={"firstName": "Patrick", "lastName": "Shechet"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"hello": "Patrick Shechet"})


if __name__ == "__main__":
    main()
