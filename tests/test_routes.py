from random import random

import pytest
from copy import deepcopy
import io
import json
from conftest import names
from app.models import User, Tweet, Like, Follow


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


# подписываем всех друг на друга
def test_post_follow(client, _db):
    users = {
        user.name: user.id
        for user in _db.session.query(User).filter(User.name.in_(names)).all()
    }
    for name in names:
        to_follows = deepcopy(names)
        to_follows.remove(name)
        for follow in to_follows:
            resp = client.post(
                f"/api/users/{users[follow]}/follow", headers=get_head(name)
            )
            assert resp.status_code == 201


# лайкаем все посты на кого подписаны от имени одного пользователя
def test_post_like(client, _db):
    users = {
        user.name: user.id
        for user in _db.session.query(User).filter(User.name.in_(names)).all()
    }
    for user in users:
        # находим всех на кого подписаны
        followings = (
            _db.session.query(User.following).filter(User.id == users[user]).all()
        )

        # отправляем лайк каждому посту
        for follow in followings:
            resp = client.post(
                f"/api/tweets/{follow.tweets.id}/likes", headers=get_head(users[user])
            )
            assert resp.status_code == 201


def test_get_api_user_id(client, _db):
    users = {
        user.name: user.id
        for user in _db.session.query(User).filter(User.name.in_(names)).all()
    }
    for user_name, user_id in users.items():
        resp = client.get(f"/api/users/{user_id}", headers=get_head(user_name))
        assert resp.status_code == 200
        resp_data = json.loads(resp.data.decode())
        assert resp_data["result"] == "true"
        assert all(map(resp_data.__contains__, ("result", "user")))
        assert all(
            map(
                resp_data["user"].__contains__, ("id", "name", "followers", "following")
            )
        )


def test_delete_like(client, _db):
    assert len(_db.session.query(Like).all()) > 0
    users = {
        user.name: user.id
        for user in _db.session.query(User).filter(User.name.in_(names)).all()
    }
    for user in users:
        # находим всех на кого подписаны
        followings = (
            _db.session.query(User.following).filter(User.id == users[user]).all()
        )

        # удаляем лайк каждому посту
        for follow in followings:
            resp = client.delete(
                f"/api/tweets/{follow.tweets.id}/likes", headers=get_head(users[user])
            )
            assert resp.status_code == 200
    assert len(_db.session.query(Like).all()) == 0


def test_delete_tweet(client, _db):
    all_tweets_id = _db.session.query(Tweet).all()
    assert len(all_tweets_id) > 0
    for tweet in all_tweets_id:
        resp = client.delete(
            f"/api/tweets/{tweet.id}", headers=get_head(tweet.author.name)
        )
        assert resp.status_code == 200
    assert len(_db.session.query(Tweet).all()) == 0


def test_delete_follow(client, _db):
    assert len(_db.session.query(Follow).all()) > 0
    users = {
        user.name: user.id
        for user in _db.session.query(User).filter(User.name.in_(names)).all()
    }
    for user_name, user_id in users.items():
        # находим всех на кого подписаны
        followings = _db.session.query(User.following).filter(User.id == user_id).all()

        # удаляем подписки
        for follow in followings:
            resp = client.delete(
                f"/api/users/{follow.following_id}/follow", headers=get_head(user_name)
            )
            assert resp.status_code == 200
    assert len(_db.session.query(Follow).all()) == 0