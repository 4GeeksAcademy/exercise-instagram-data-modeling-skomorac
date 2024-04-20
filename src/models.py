import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.user_id'))
    receiver_id = Column(Integer, ForeignKey('users.user_id'))
    creation_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    sender = relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='received_messages')


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key = True)
    full_name = Column(String(200), nullable = False)
    username = Column(String(50), unique = True, nullable = False)
    password = Column(String(50), nullable = False)
    profile_picture = Column(String(200), nullable = False)
    creation_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    posts = relationship('Post', back_populates = 'user')
    favorites = relationship('Favorites', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    shared_posts = relationship('SharePost', back_populates='user')
    
    sent_messages = relationship('Message', foreign_keys=[Message.sender_id], back_populates='sender')
    received_messages = relationship('Message', foreign_keys=[Message.receiver_id], back_populates='receiver')

class Post(Base):
    __tablename__ = 'posts'

    post_id = Column(Integer, primary_key = True)
    creation_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    user_id = Column(Integer, ForeignKey('users.user_id'))

    user = relationship('User', back_populates = 'posts')
    media = relationship('Media', back_populates = 'post')
    favorites = relationship('Favorites', back_populates='post')
    comments = relationship('Comment', back_populates='post')
    shared_users = relationship('SharePost', back_populates='post')


class Media(Base):
    __tablename__ = 'media'

    media_id = Column(Integer, primary_key = True)
    media_type = Column(String(100), nullable = False)
    media_url = Column(String(250), nullable = False)
    post_id = Column(Integer, ForeignKey('posts.post_id'))

    posts = relationship('Post', back_populates = 'media')

class Favorites(Base):
    __tablename__ = 'favorites'

    favorite_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post_id = Column(Integer, ForeignKey('posts.post_id'))

    user = relationship('User', back_populates='favorites')
    post = relationship('Post', back_populates='favorites')

class Comment(Base):
    __tablename__ = 'comments'

    comment_id = Column(Integer, primary_key=True)
    text = Column(String(500), nullable=False)
    creation_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post_id = Column(Integer, ForeignKey('posts.post_id'))

    user = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class SharePost(Base):
    __tablename__ = 'share_posts'

    share_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    post_id = Column(Integer, ForeignKey('posts.post_id'))
    share_date = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    user = relationship('User', back_populates='shared_posts')
    post = relationship('Post', back_populates='shared_users')


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
