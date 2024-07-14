from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    api_key = Column(String(100), unique=True, index=True)
    tweets = relationship("Tweet", back_populates="author")
    following = relationship("Follow", back_populates="follower", foreign_keys="[Follow.follower_id]")
    followers = relationship("Follow", back_populates="followed", foreign_keys="[Follow.followed_id]")
    likes = relationship("Like", back_populates="user")

class Tweet(Base):
    __tablename__ = "tweets"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(280))
    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship("User", back_populates="tweets")
    likes = relationship("Like", back_populates="tweet")
    media = relationship("Media", back_populates="tweet")

class Follow(Base):
    __tablename__ = "follows"
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('users.id'))
    followed_id = Column(Integer, ForeignKey('users.id'))
    follower = relationship("User", back_populates="following", foreign_keys=[follower_id])
    followed = relationship("User", back_populates="followers", foreign_keys=[followed_id])

class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tweet_id = Column(Integer, ForeignKey('tweets.id'))
    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String(200))
    tweet_id = Column(Integer, ForeignKey('tweets.id'))
    tweet = relationship("Tweet", back_populates="media")
