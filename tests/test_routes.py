import pytest
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
        assert "followers" in resp_data["user"]
        assert "following" in resp_data["user"]


# post api/tweets
def post_tweets(client, _db):
    for name in names:
        resp = client.post("api/tweets", headers=get_head(name))
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

        # оправляем сам твит, с id картинок
        content = {
            "tweet_data": "тестовая запись в бд 2131",
            "tweet_media_ids": media_id,
        }
        resp = client.post("api/tweets", data=content, headers=get_head(name))
        assert resp.status_code == 201
        assert resp_data["result"] == "true"
        assert isinstance(resp_data["tweet_id"], int)

        # проверка с базой
        user_id = _db.session.query(User).filter_by(name=name).first()
        tweet_instance = _db.session.query(Tweet).filter_by(user_id=user_id)
        image_instance = _db.session.query(Image).filter_by(tweet_id)
        assert tweet_instance.content == content["tweet_data"]


# get api/tweets
def get_tweets(client, _db):
    pass
