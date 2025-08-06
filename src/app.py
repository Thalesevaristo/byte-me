import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import db


migrate = Migrate()
jwt = JWTManager()


def create_app(environment=os.environ["ENVIRONMENT"]):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(
        f"src.config.{environment.title()}Config",
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from src.routes import user, post, auth

    app.register_blueprint(user.app)
    app.register_blueprint(post.app)
    app.register_blueprint(auth.app)

    return app
