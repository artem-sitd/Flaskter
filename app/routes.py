import os
from flask import Flask, abort, request
from flask_restful import Api, Resource
from dotenv import load_dotenv
from .models import db


def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    api = Api(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    class UsersApi(Resource):
        def get(self):
            pass

        def post(self):
            pass

        def delete(self):
            pass

    class UsersIdApi(Resource):
        def get(self):
            pass

    class TweetsApi(Resource):
        def get(self):
            pass

        def post(self):
            pass

        def delete(self):
            pass

    class TweetsIdApi(Resource):
        def post(self):
            pass

        def delete(self):
            pass

    class MediasApi(Resource):
        def post(self):
            pass

    return app
