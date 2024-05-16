from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    tweets = relationship('Tweet', back_populates='author', cascade='all, delete-orphan')
    followed = relationship('Follow', foreign_keys='Follow.follower_id', back_populates='follower',
                            cascade='all, delete-orphan')
    followers = relationship('Follow', foreign_keys='Follow.followed_id', back_populates='followed',
                             cascade='all, delete-orphan')
    likes = relationship('Like', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Tweet(db.Model):
    __tablename__ = 'tweets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(280), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship('User', back_populates='tweets')
    likes = relationship('Like', back_populates='tweet', cascade='all, delete-orphan')
    image = relationship('Image', uselist=False, back_populates='tweet', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Tweet {self.content[:20]}>'


class Follow(db.Model):
    __tablename__ = 'follows'

    id = Column(Integer, primary_key=True, autoincrement=True)
    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    followed_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    follower = relationship('User', foreign_keys=[follower_id], back_populates='followed')
    followed = relationship('User', foreign_keys=[followed_id], back_populates='followers')

    def __repr__(self):
        return f'<Follow follower_id={self.follower_id} followed_id={self.followed_id}>'


class Like(db.Model):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweets.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='likes')
    tweet = relationship('Tweet', back_populates='likes')

    def __repr__(self):
        return f'<Like user_id={self.user_id} tweet_id={self.tweet_id}>'


class Image(db.Model):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(255), nullable=False)
    tweet_id = Column(Integer, ForeignKey('tweets.id'), nullable=False)

    tweet = relationship('Tweet', back_populates='image')

    def __repr__(self):
        return f'<Image {self.url}>'
