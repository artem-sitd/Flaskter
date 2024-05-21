from functools import wraps
import os
from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource
from .config import Config
from .models import db, User, Follow, Image, Tweet, Like
from werkzeug.utils import secure_filename


def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(Config)

    api = Api(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    # проверка апи ключа, но этот способ дурной какой-то. Каждую функцию будет спамить в бд на проверку
    # почему стандартную нельзя логин и сессии ??
    # админ создал учетку, отправил логин пароль, пользователь сменил пароль на свой, браузер сохранил сессию
    def require_api_key(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            api_key = request.headers.get("Api-key")
            user = db.session.query(User).filter_by(api_key=api_key).first()
            if not user:
                user = User(name=api_key, api_key=api_key)
                db.session.add(user)
                db.session.commit()
                return {"message": "new user added"}, 201
            return f(user, *args, **kwargs)

        return decorated_function

    @app.route("/", methods=["GET"])
    def get_index():
        return render_template("index.html"), 200

    @app.route("/api/users/me", methods=["GET"])
    @require_api_key
    def get_users_me(user):
        following = [
            {"id": f.following.id, "name": f.following.name} for f in user.following
        ]

        followers = [
            {"id": f.follower.id, "name": f.follower.name} for f in user.followers
        ]
        return {
            "result": "true",
            "user": {
                "id": user.id,
                "name": user.name,
                "followers": followers,
                "following": following,
            },
        }, 200

    class UsersIdApi(Resource):
        # /api/users/id
        def get(self, id):
            user = db.session.get(User, id)
            if not user:
                return err("не верный юзер", None)

            following = [
                {"id": follow.following.id, "name": follow.following.name}
                for follow in user.following
            ]

            followers = [
                {"id": f.follower.id, "name": f.follower.name} for f in user.followers
            ]

            return {
                "result": "true",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "followers": followers,
                    "following": following,
                },
            }

    class TweetsApi(Resource):
        method_decorators = [require_api_key]

        def get(self, user):
            followings = db.session.query(Follow).filter_by(follower_id=user.id).all()
            if not followings:
                return {"result": True}, 200
            result = []
            for following in followings:
                # Извлечение твитов пользователей, на которых подписан текущий пользователь
                tweets = (
                    db.session.query(Tweet)
                    .filter_by(user_id=following.following_id)
                    .all()
                )
                for tweet in tweets:
                    attachments = (
                        [image.url for image in tweet.image] if tweet.image else []
                    )

                    result.append(
                        {
                            "id": tweet.id,
                            "content": tweet.content,
                            "attachments": attachments,
                            "author": {
                                "id": tweet.author.id,
                                "name": tweet.author.name,
                            },
                            "likes": [
                                {"user_id": like.user.id, "name": like.user.name}
                                for like in tweet.likes
                            ],
                        }
                    )
            return {"result": True, "tweets": result}, 200

        def post(self, user):
            content = request.json.get("tweet_data")
            if not content:
                return err("no content in tweet", None), 400
            new_tweet = Tweet(content=content, user_id=user.id)
            db.session.add(new_tweet)
            db.session.commit()

            media = request.json.get("tweet_media_ids")
            if media:
                images = db.session.query(Image).filter(Image.id.in_(media)).all()
                for image in images:
                    image.tweet_id = new_tweet.id
                db.session.commit()
            return {"result": True, "tweet_id": new_tweet.id}, 201

    class TweetsIdApi(Resource):
        def delete(self, id):
            tweet = db.session.get(Tweet, id)
            if not tweet:
                return err("does not exists tweet by id", None), 400
            db.session.delete(tweet)
            db.session.commit()
            return {"result": True}

    class MediasApi(Resource):
        # decorators = [require_api_key]

        def post(self):
            file = request.files["file"]
            if not file:
                return err("not file in form", None), 400

            if file.filename == "":
                return err("No selected file", None), 400

            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            media = Image(url=filepath, tweet_id=None)
            db.session.add(media)
            db.session.commit()
            return {"result": True, "media_id": media.id}

    class TweetsIdLikes(Resource):
        method_decorators = [require_api_key]

        def post(self, user, id):
            tweet = db.session.get(Tweet, id)
            if not tweet:
                return err("does not exists tweet by id", None), 400
            new_like = Like(user_id=user.id, tweet_id=tweet.id)
            db.session.add(new_like)
            db.session.commit()
            return {"result": True}

        def delete(self, user, id):
            tweet = db.session.get(Tweet, id)
            if not tweet:
                return err("does not exists tweet by id", None), 400
            like_to_delete = (
                db.session.query(Like)
                .filter_by(user_id=user.id, tweet_id=tweet.id)
                .first()
            )
            if not like_to_delete:
                return err("not like on this post and this user", None), 400
            db.session.delete(like_to_delete)
            db.session.commit()
            return {"result": True}

    class UsersIdFollow(Resource):
        method_decorators = [require_api_key]

        def post(self, user, id):
            user_to_follow = db.session.query(User).get(id)
            if user.id == id:
                return err("You cannot follow yourself", None), 400

            # Найти пользователя, на которого нужно подписаться
            if not user_to_follow:
                return err("User not found", None), 404

                # Проверить, что пользователь в данный момент не подписан на этого пользователя
            follow_exists = (
                db.session.query(Follow)
                .filter_by(follower_id=user.id, following_id=user_to_follow.id)
                .first()
            )
            if follow_exists:
                return err("You are already following this user", None), 400
            new_follow = Follow(follower_id=user.id, following_id=user_to_follow.id)
            db.session.add(new_follow)
            db.session.commit()
            return {"result": "true"}, 201

        def delete(self, user, id):
            user_to_unfollow = db.session.query(User).get(id)
            if user.id == id:
                return err("You cannot unfollow yourself", None), 400

            if not user_to_unfollow:
                return err("User not found", None), 404

            # проверить что подписка существует
            follow_exists = (
                db.session.query(Follow)
                .filter_by(follower_id=user.id, following_id=user_to_unfollow.id)
                .first()
            )
            if not follow_exists:
                return err("You are not following this user", None), 400
            db.session.delete(follow_exists)
            db.session.commit()
            return {"result": "true"}, 200

    api.add_resource(TweetsApi, "/api/tweets")  # post, get

    api.add_resource(TweetsIdApi, "/api/tweets/<int:id>")  # delete

    api.add_resource(TweetsIdLikes, "/api/tweets/<int:id>/likes")  # delete, post

    api.add_resource(UsersIdFollow, "/api/users/<int:id>/follow")  # post, delete

    api.add_resource(UsersIdApi, "/api/users/<int:id>")  # get

    api.add_resource(MediasApi, "/api/medias")  # post

    return app


def err(type, mes):
    return {"result": False, "error_type": type, "error_message": mes}
