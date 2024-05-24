import io
import json
import sys
from copy import deepcopy
from random import random

import pytest

from app.models import Follow, Like, Tweet, User

from .conftest import names


def get_head(api_key, content_type=None):
    if content_type:
        return {"Api-key": api_key, "Content-type": content_type}
    return {"Api-key": api_key}


# localhost
def test_index(client, db):
    for name in names:
        resp = client.get("/", headers=get_head(name))
        assert resp.status_code == 200
        check_indb = (
            db.session.query(User.name).filter_by(name=name).first() is not None
        )
        assert check_indb is True


# /api/users/me
def test_get_users_me(client, db):
    for name in names:
        resp = client.get("/api/users/me", headers=get_head(name))
        assert resp.status_code == 200
        resp_data = json.loads(resp.data.decode())
        assert resp_data["result"] == "true"
        assert "user" in resp_data
        assert "id" in resp_data["user"]
        assert resp_data["user"]["name"] == name
        assert all(key in resp_data["user"] for key in ("followers", "following"))


# post api/tweets
def test_post_tweets(client, db):
    for name in names:
        resp = client.post("api/tweets", headers=get_head(name))
        # отправляем без контента
        assert resp.status_code == 400 or resp.status_code == 415

        # сначала отправляем картинку (имитацию картинки), только потом tweet
        data = {"file": (io.BytesIO(b"test image content"), f"test_image_{name}.jpg")}
        resp = client.post(
            "api/medias",
            data=data,
            headers=get_head(name, "multipart/form-data"),
        )
        assert resp.status_code == 200
        resp_data = json.loads(resp.data.decode())
        assert resp_data["result"] is True
        media_id = resp_data["media_id"]

        # создаем твит
        content = {
            "tweet_data": "тестghgая запись в бд 2131",
            "tweet_media_ids": [media_id],
        }
        resp = client.post(
            "api/tweets",
            json=content,
            headers=get_head(name, "application/json"),
        )
        resp_data = json.loads(resp.data.decode())

        assert resp.status_code == 201
        assert resp_data["result"] is True
        assert isinstance(resp_data["tweet_id"], int)

        # проверка контента твитов в бд
        user = db.session.query(User).filter_by(name=name).first()
        for user_tweet in user.tweets:
            assert user_tweet.user_id == user.id
            assert user_tweet.content == content["tweet_data"]


# подписываем всех друг на друга
def test_post_follow(client, db):
    assert len(db.session.query(Follow).all()) == 0
    users = {
        user.name: user.id
        for user in db.session.query(User).filter(User.name.in_(names)).all()
    }
    for user_name, user_id in users.items():
        to_follows = deepcopy(names)
        to_follows.remove(user_name)
        for follow in to_follows:
            resp = client.post(
                f"/api/users/{users[follow]}/follow", headers=get_head(user_name)
            )
            assert resp.status_code == 201
    assert len(db.session.query(Follow).all()) > 0


# get api/tweets
def test_get_tweets(client, db):
    for name in names:
        resp = client.get("api/tweets", headers=get_head(name))
        assert resp.status_code == 200 or resp.status_code == 201
        resp_data = json.loads(resp.data.decode())
        assert all(
            key in resp_data["tweets"][0]
            for key in ("id", "content", "attachments", "author", "likes")
        )


# лайкаем все посты на кого подписаны от имени одного пользователя
def test_post_like(client, db):
    assert len(db.session.query(Like).all()) == 0
    users = {
        user.name: user.id
        for user in db.session.query(User).filter(User.name.in_(names)).all()
    }
    for user_name, user_id in users.items():
        # находим всех на кого подписаны
        my_followings = db.session.query(Follow).filter_by(follower_id=user_id).all()

        # находим все посты на кого подписаны
        tweets_my_following = [
            tweet for follow in my_followings for tweet in follow.following.tweets
        ]
        # отправляем лайк каждому посту
        for tweet in tweets_my_following:
            resp = client.post(
                f"/api/tweets/{tweet.id}/likes", headers=get_head(user_name)
            )
            assert resp.status_code == 201

    assert len(db.session.query(Like).all()) > 0


def test_get_api_user_id(client, db):
    users = {
        user.name: user.id
        for user in db.session.query(User).filter(User.name.in_(names)).all()
    }
    for user_name, user_id in users.items():
        resp = client.get(f"/api/users/{user_id}", headers=get_head(user_name))
        assert resp.status_code == 200
        resp_data = json.loads(resp.data.decode())
        assert resp_data["result"] == "true"
        assert all(key in resp_data.keys() for key in ("result", "user"))
        assert all(
            key in resp_data["user"] for key in ("id", "name", "followers", "following")
        )


def test_delete_like(client, db):
    assert len(db.session.query(Like).all()) > 0
    users = {
        user.name: user.id
        for user in db.session.query(User).filter(User.name.in_(names)).all()
    }
    for user_name, user_id in users.items():
        # находим всех на кого подписаны
        my_followings = db.session.query(Follow).filter_by(follower_id=user_id).all()

        # находим все посты на кого подписаны
        tweets_my_following = [
            tweet for follow in my_followings for tweet in follow.following.tweets
        ]
        # отправляем лайк каждому посту
        for tweet in tweets_my_following:
            resp = client.delete(
                f"/api/tweets/{tweet.id}/likes", headers=get_head(user_name)
            )
            assert resp.status_code == 200

    assert len(db.session.query(Like).all()) == 0


def test_delete_tweet(client, db):
    all_tweets_id = db.session.query(Tweet).all()
    assert len(all_tweets_id) > 0
    for tweet in all_tweets_id:
        resp = client.delete(
            f"/api/tweets/{tweet.id}", headers=get_head(tweet.author.name)
        )
        assert resp.status_code == 200
    assert len(db.session.query(Tweet).all()) == 0


def test_delete_follow(client, db):
    assert len(db.session.query(Follow).all()) > 0
    users = {
        user.name: user.id
        for user in db.session.query(User).filter(User.name.in_(names)).all()
    }
    for user_name, user_id in users.items():
        # находим всех на кого подписаны
        my_followings = db.session.query(Follow).filter_by(follower_id=user_id).all()

        # удаляем подписки
        for follow in my_followings:
            resp = client.delete(
                f"/api/users/{follow.following_id}/follow", headers=get_head(user_name)
            )
            assert resp.status_code == 200
    assert len(db.session.query(Follow).all()) == 0
