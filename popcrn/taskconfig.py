import os
import logging

from popcrn.models import DBSession

from ConfigParser import SafeConfigParser

from sqlalchemy import create_engine

from celery import (
    Celery,
    Task
)

from celery.signals import worker_init

settings = SafeConfigParser()
settings.read(os.environ.get("POPCRN_INI", "development.ini"))

DB_URL = settings.get("app:main", "sqlalchemy.url")

@worker_init.connect
def bootstrap_pyramid(signal, sender):
    pass

CELERY_CONFIG = "popcrn.celeryconfig"

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
        logger.info("PERSISTING tweet: {}".format(tweet.tweet_id))
        existing_tweet = self.db.query(Tweet).filter(Tweet.tweet_id == tweet.tweet_id).first()

        if not existing_tweet:
            tweet_record = Tweet(
                created=datetime.utcnow(),
                tweet_id=tweet.tweet_id,
                user_id=tweet.user_id,
                user_screen_name=tweet.user_screen_name,
                url=tweet.url
            )
            self.db.add(tweet_record)
            self.info("STORING tweet_record: {}".format(tweet_record))
            self.commit()
        else:
            logger.info("NOT PERSISTING tweet: {}. Already ingested.".format(tweet.tweet_id))

    def persist_tweets(self, tweets=[]):
        for tweet in tweets:
            persist_tweet(tweet)
