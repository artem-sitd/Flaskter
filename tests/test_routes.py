import pytest
from copy import deepcopy
import io
import json
from conftest import names
from app.models import User, Tweet, Image


def get_head(api_key):
    return {"Api-key": api_key}


# localhost
def test_index(client, _db):
    for name in names:
        resp = client.get("/", headers=get_head(name))
        assert resp.status_code == 200
        check_in_db = (
            _db.session.query(User.name).filter_by(name=name).first() is not None
        )
        assert check_in_db is True


# /api/users/me
def test_get_users_me(client, _db):
    for name in names:
        resp = client.get("/api/users/me", headers=get_head(name))
        assert resp.status_code == 200
        resp_data = json.loads(resp.data.decode())
        assert resp_data["result"] == "true"
        assert "user" in resp_data
        assert "id" in resp_data["user"]
        assert resp_data["user"]["name"] == name
        assert (
            all(map(resp_data["user"].__contains__, ("followers", "following"))) is True
        )
        # assert "followers" in resp_data["user"]
        # assert "following" in resp_data["user"]


# post api/tweets
def test_post_tweets(client, _db):
    for name in names:
        resp = client.post("api/tweets", headers=get_head(name))
        # отправляем без контента
        assert resp.status_code == 400

        # сначала отправляем картинку (имитацию картинки), только потом tweet
        data = {"file": (io.BytesIO(b"test image content"), "test_image.jpg")}
        resp = client.post(
            "api/medias",
            data=data,
            content_type="multipart/form-data",
            headers=get_head(name),
        )
        assert resp.status_code == 201
        resp_data = json.loads(resp.data.decode())
        assert resp_data["result"] == "true"
        media_id = resp_data["media_id"]

        # создаем твит
        content = {
            "tweet_data": "тестовая запись в бд 2131",
            "tweet_media_ids": media_id,
        }
        resp = client.post("api/tweets", data=content, headers=get_head(name))
        assert resp.status_code == 201
        assert resp_data["result"] == "true"
        assert isinstance(resp_data["tweet_id"], int)

        # проверка контента твитов в бд
        user = _db.session.query(User).filter_by(name=name).first()
        for user_tweet in user.tweets:
            assert user_tweet.user_id == user.id
            assert user_tweet.content == content["tweet_data"]


# get api/tweets
def test_get_tweets(client, _db):
    for name in names:
        resp = client.get("api/tweets", headers=get_head(name))
        assert resp.status_code == 200
        resp_data = json.loads(resp.data.decode())
        assert (
            all(
                map(
                    resp_data.__contains__,
                    ("id", "content", "attachments", "author", "likes"),
                )
            )
            is True
        )


def test_post_follow(client, _db):
    users = {
        user.name: user.id for user in User.query.filter(User.name.in_(names)).all()
    }
    subscriptions = []

    for name in names:
        follower_id = users[name]
        new_names = deepcopy(names)
        new_names.remove(name)
        resp = client.post("/api/users/<id>/follow", headers=get_head(name))
        # отправляем без контента
        assert resp.status_code == 400
    pass


def test_post_like(client, _db):
    pass


def test_get_api_user_id(client, _db):
    pass


def test_delete_tweet(client, _db):
    pass


def test_delete_like(client, _db):
    pass


def test_delete_follow(client, _db):
    pass
