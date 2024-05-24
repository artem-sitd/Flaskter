import pytest
from dotenv import load_dotenv

from app.config import ConfigTest
from app.models import User
from app.models import db as _db
from app.routes import create_app

names = {"vasya12", "petya32", "15gevorg", "tor", "odin"}


@pytest.fixture(scope="module")
def app():
    load_dotenv()
    _app = create_app()

    _app.config["TESTING"] = True
    _app.config.from_object(ConfigTest)

    _db.init_app(_app)

    with _app.app_context():
        _db.create_all()

        """Далее создаются несколько юзеров Напрямую в бд"""
        for name in names:
            new_user = User(name=name, api_key=name)
            _db.session.add(new_user)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture(scope="module")
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture(scope="module")
def db(app):
    with app.app_context():
        yield _db
