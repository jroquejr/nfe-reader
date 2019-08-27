from flask import Flask


def create_app():
    app = Flask(__name__.split(".")[0])

    from . import api

    app.register_blueprint(api.blueprint)

    return app
