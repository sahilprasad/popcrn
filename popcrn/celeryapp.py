import os
import logging

import json

import ast

from datetime import datetime

from popcrn.models import (
    RawSession,
    Tweet
)

from popcrn.util.task_utils import parse_tweet_datetime

from popcrn.sentiment.analyzer import SentimentAnalyzer

from ConfigParser import SafeConfigParser

from sqlalchemy import create_engine

from celery import (
    Celery,
    Task
)

from celery.signals import worker_init

sentiment = SentimentAnalyzer()

settings = SafeConfigParser()
settings.read(os.environ.get("POPCRN_INI", "development.ini"))

DB_URL = settings.get("app:main", "sqlalchemy.url")

@worker_init.connect
def bootstrap_pyramid(signal, sender):
    pass

CELERY_CONFIG = "celeryconfig"

app = Celery()
app.config_from_object(CELERY_CONFIG)

logger = logging.getLogger(__name__)

class HarvestTask(Task):
    abstract = True

    def __init__(self, db_url=None):
        self.db_url = db_url or DB_URL
        self._db = None

    @property
    def db(self):
        if self._db is None:
            engine = create_engine(self.db_url)
            self._db = RawSession(bind=engine)
        return self._db

    def commit(self):
        logger.info("COMMIT")
        if self._db:
            self._db.commit()

    def rollback(self):
        logger.info("ROLLBACK")
        if self._db:
            self._db.rollback()

    def close(self):
        logger.info("CLOSE")
        if self._db:
            self._db.close()
            self._db = None

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.rollback()
        self.close()

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        self.rollback()
        self.close()

    def get_tweets_of_user(self, user_id=None, screen_name=None):
        if not user_id and not screen_name:
            logger.error("HarvestTask: get_tweets_of_user called without one of user_id/screen_name")
            return []

        query = self.db.query(Tweet).filter(Tweet.user_id == user_id)
        if not user_id:
            query = self.db.query(Tweet).filter(Tweet.user_screen_name == screen_name)

        return query.all()

    def persist_tweet(self, tweet):
        tweet_id_orig = tweet["id"]
        logger.info("PERSISTING tweet: {}".format(tweet_id_orig))
        existing_tweet = self.db.query(Tweet).filter(Tweet.tweet_id == tweet["id"]).first()
        logger.error("EXISTING TWEET: {}".format(existing_tweet))
        if existing_tweet is None:
            sentiments = sentiment.generate_mapping(tweet["text"])
            avg_sentiment = sum(sentiments.values()) / len(sentiments.values())
            max_sentiment_word = [
                k for k, v in sentiments.iteritems() if v == max(sentiments.values())
            ][0]
            max_sentiment_word_value = sentiments[max_sentiment_word]

            min_sentiment_word = [
                k for k, v in sentiments.iteritems() if v == min(sentiments.values())
            ][0]
            min_sentiment_word_value = sentiments[min_sentiment_word]

            tweet = Tweet(
                created=parse_tweet_datetime(tweet["created_at"]),
                user_id=tweet["user"]["id"],
                tweet_id=tweet["id"],
                text=tweet["text"],
                user_screen_name=tweet["user"]["screen_name"],
                topic=tweet["topic"],
                sentiment=avg_sentiment,
                max_sentiment_word=max_sentiment_word,
                max_sentiment_word_value=max_sentiment_word_value,
                min_sentiment_word=min_sentiment_word,
                min_sentiment_word_value=min_sentiment_word_value
            )
            self.db.add(tweet)
            logger.info("STORING tweet_record: {}".format(tweet_id_orig))
            self.commit()
        else:
            logger.info("NOT PERSISTING tweet: {}. Already ingested.".format(tweet_id_orig))

    def persist_tweets(self, tweets=[]):
        for tweet in tweets:
            self.persist_tweet(tweet)

    def persist_tweets_json(self, tweets=[]):
        for tweet_json in tweets:
            tweet = json.loads(tweet_json)
            if validate_tweet_json(tweet):
                tweet_id = tweet["id"]

                existing_tweet = self.db.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()
                if not existing_tweet:
                    record = Tweet(
                        tweet_id=tweet["id"],
                        user_id=tweet["user"]["id"],
                        user_screen_name=tweet["user"]["screen_name"],
                        created=parse_tweet_datetime(tweet["created_at"]),
                        text=tweet["text"]
                    )
                    self.db.add(record)
                    self.info("STORING tweet: {}",format(record))
                    self.commit()
