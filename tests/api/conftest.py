from pytest import fixture

from api.app import create_app


@fixture
def app():
    return create_app({"TESTING": True})


@fixture
def client(app):
    return app.test_client()
