from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy as sa
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension

from sqlalchemy import (
    Column, Integer, UnicodeText, DateTime, String
)

RawSession = sessionmaker()
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()

class Tweet(Base):
    __tablename__ = 'tweet'
    tweet_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    user_screen_name = Column(String)
    created = Column(DateTime, nullable=False)
    url = Column(String, nullable=False)
