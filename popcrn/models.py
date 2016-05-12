from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy import (
    Column, Integer, UnicodeText, DateTime, String, Table, ForeignKey
)

RawSession = sessionmaker()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()

mapping = Table(
    'association', Base.metadata,
    Column(
        'tweet_id',
        Integer,
        ForeignKey('tweet.tweet_id')
    ),
    Column(
        'sentiment_id',
        Integer,
        ForeignKey('sentiment.sentiment_id')
    )
)

class Tweet(Base):
    __tablename__ = 'tweet'
    tweet_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    user_screen_name = Column(String(100))
    created = Column(DateTime, nullable=False)
    text = Column(String(150), nullable=False)

    max_sentiment_word = Column(String(150))
    min_sentiment_word = Column(String(150))

    sentiments = relationship(
        "Sentiment",
        secondary=mapping,
        back_populates="tweets"
    )

    user_id = Column(Integer, ForeignKey('user.user_id'))

class Sentiment(Base):
    __tablename__ = 'sentiment'
    sentiment_id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    topic = Column(String(100), nullable=False, index=True)
    value = Column(String(100))

    tweets = relationship(
        "Tweet",
        secondary=mapping,
        back_populates="sentiments")

class User(Base):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    location = Column(String(100))
    country_code = Column(String(10), nullable=False, default="US")

    tweets = relationship('tweets')
