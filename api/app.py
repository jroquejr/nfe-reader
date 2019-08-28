from flask import Flask


def create_app():
    app = Flask(__name__.split(".")[0])

    from . import views

    app.register_blueprint(views.blueprint)

    return app
