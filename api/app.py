from flask import Flask


def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.update(config)

    from . import views

    app.register_blueprint(views.blueprint)

    return app
