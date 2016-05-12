from popcrn.celeryapp import (
    app,
    HarvestTask
)

from popcrn.models import (
    Tweet,
    User,
    Sentiment
)

from popcrn.util.task_utils import (
    parse_tweet_datetime,
    validate_tweet_json
)

from popcrn.ingestion.apis.twitter import Twitter
from datetime import datetime

import logging

import ast

logger = logging.getLogger(__name__)

twitter = Twitter()

TWEET_FETCH_SIZE = 50

@app.task(base=HarvestTask, bind=True, ignore_result=True, rate_limit='1/m')
def geo_harvest(self, user_id):
    obj = self.db.query(User).filter(User.user_id == int(user_id)).first()
    if not obj:
        logger.error("Geo harvest did not found user in database: {}".format(user_id))
        return

    if not obj.location:
        logger.error("Geo harvest did not find a location to search the Twitter API for.")
        return

    resp = twitter.get_country_code(query=obj.location, granularity="country", max_results=1)
    if not resp.get("result") and not resp["result"].get("country_code"):
        logger.error("Could not find country_code attribute for user_id {}: {}".format(user_id, resp))
    else:
        logger.info("Found country_code for user_id {}: {}".format(user_id,
            resp["result"]["country_code"]))
        obj.country_code = resp["result"]["country_code"]
        self.commit()

@app.task(base=HarvestTask, bind=True, ignore_result=True)
def topic_harvest(self, topic=None):
    tweet_json = twitter.get_topic_tweets(topic=topic, include_rts=False,
        exclude_replies=True, count=100)

    tweets = []
    for tweet in tweet_json["statuses"]:
        logger.info("Examining tweet: {}".format(tweet))
        if validate_tweet_json(tweet):
            user_id = tweet["user"]["id"]
            user_object = self.db.query(User).filter(User.user_id == user_id).first()
            if not user_object:
                user_object = User(
                    user_id=user_id,
                    created=datetime.utcnow(),
                    location=tweet["user"]["location"]
                )
                # logger.info("User location: {}".format(tweet["user"]["location"]))
                print tweet["user"]["location"]
                self.db.add(user_object)
                self.commit()
                logger.info("enqueueing geo harvest for user: {}".format(user_id))
                geo_harvest.delay(user_id)

            tweets.append(Tweet(
                tweet_id=tweet["id"],
                text=tweet["text"],
                user_screen_name=tweet["user"]["screen_name"],
                user_id=tweet["user"]["id"],
                created=parse_tweet_datetime(tweet["created_at"])
            ))

            self.persist_tweet(tweet)

    return tweets

@app.task(base=HarvestTask, bind=True, ignore_result=True, rate_limit='5/m')
def import_user_tweets(self, user_id=None, screen_name=None, **kwargs):
    tweet_json = twitter.get_user_tweets(user_id=user_id, screen_name=screen_name,
        include_rts=False, exclude_replies=True, count=TWEET_FETCH_SIZE, **kwargs)

    tweets = []
    for tweet in tweet_json:
        if (validate_tweet_json(tweet)):
            tweets.append(Tweet(
                tweet_id=tweet["id"],
                text=tweet["text"],
                user_screen_name=tweet["user"]["screen_name"],
                user_id=tweet["user"]["id"],
                created=parse_tweet_datetime(tweet["created"])
            ))

            self.persist_tweet(tweet)

    return tweets
