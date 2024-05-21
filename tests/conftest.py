import pytest
from dotenv import load_dotenv
from app.routes import create_app
from app.config import ConfigTest
from app.models import User, db as _db


names = {"vasya12", "petya32", "15gevorg", "tor", "odin"}


@pytest.fixture
def app():
    load_dotenv()
    _app = create_app()
    _app.config.from_object(ConfigTest)
    _app.config["TESTING"] = True

    with _app.app_context():
        _db.create_all()

        """Далее создаются несколько юзеров Напрямую в бд"""
        for name in names:
            new_user = User(name=name, api_key=name)
            _db.session.add(new_user)
        _db.session.commit()

        yield app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db