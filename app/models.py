from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    api_key = Column(String(50), unique=True, nullable=False)

    tweets = relationship(
        "Tweet", back_populates="author", cascade="all, delete-orphan"
    )

    # НА КОГО Я ПОДПИСАН!
    following = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",
    )

    # Пользователи, которые подписаны на этого пользователя
    followers = relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        back_populates="following",
        cascade="all, delete-orphan",
    )

    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.name}>"


class Follow(db.Model):
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, autoincrement=True)

    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    follower = relationship(
        "User", foreign_keys="Follow.follower_id", back_populates="following"
    )
    following = relationship(
        "User", foreign_keys="Follow.following_id", back_populates="followers"
    )


def __repr__(self):
    return f"<Follow follower_id={self.follower_id} followed_id={self.followed_id}>"


class Tweet(db.Model):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(280), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    author = relationship("User", back_populates="tweets")
    likes = relationship("Like", back_populates="tweet", cascade="all, delete-orphan")
    image = relationship(
        "Image", back_populates="tweet", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Tweet {self.content[:20]}>"


class Like(db.Model):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")

    def __repr__(self):
        return f"<Like user_id={self.user_id} tweet_id={self.tweet_id}>"


class Image(db.Model):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id"), nullable=True)

    tweet = relationship("Tweet", back_populates="image")

    def __repr__(self):
        return f"<Image {self.url}>"
