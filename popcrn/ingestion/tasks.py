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

import urllib

from popcrn.ingestion.apis.twitter import Twitter
from datetime import datetime, timedelta

import logging
import pycountry

import ast

logger = logging.getLogger(__name__)

twitter = Twitter()

TWEET_FETCH_SIZE = 50

@app.task(base=HarvestTask, bind=True, ignore_result=True, rate_limit='1/m')
def geo_harvest(self, user_id):
    obj = self.db.query(User).filter(User.user_id == user_id).first()
    if not obj:
        logger.error("Geo harvest did not found user in database: {}".format(user_id))
        return

    if not obj.location:
        logger.error("Geo harvest did not find a location to search the " +
            " Twitter API for: loc: {}, user_id: {}".format(obj.location, user_id))
        return

    loc = obj.location;
    try:
        loc = urllib.quote_plus(obj.location)
    except KeyError:
        pass

    resp = twitter.get_country_code(query=loc, granularity="city", max_results=1)
    if resp.get("result") is not None:
        if resp["result"].get("places"):
            place = resp["result"]["places"][0]
            logger.info("Found place for user_id: {}".format(place))
            alpha2 = resp["result"]["places"][0].get("country_code")
            if alpha2 is not None:
                country = pycountry.countries.get(alpha2=alpha2)
                if country:
                    logger.info("COUNTRY CODE FOR {}: {}".format(user_id,
                        country.alpha3))
                    obj.country_code = country.alpha3
            self.commit()
        else:
            logger.error("Could not find country code for user: {}".format(user_id))
    else:
        logger.error("Could not find country_code for user: {} - {}".format(user_id, resp))


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
            sentiment_object = self.db.query(Sentiment).filter(Sentiment.topic == topic).first()
            if not user_object:
                user_object = User(
                    user_id=user_id,
                    created=datetime.utcnow(),
                    location=tweet["user"]["location"]
                )
                print tweet["user"]["location"]
                self.db.add(user_object)
                self.commit()
                logger.info("enqueueing geo harvest for user: {}".format(user_id))
                geo_harvest.delay(user_id) #
            if not sentiment_object:
                sentiment_object = Sentiment(
                    created=datetime.now(),
                    topic=topic
                )
                logger.info("created new Sentiment object: {}".format(topic))
            tweet["topic"] = topic

            self.persist_tweet(tweet)

    next_harvest = datetime.now() + timedelta(minutes=10)
    self.apply_async(args=[topic], eta=next_harvest)
    return tweets

@app.task(base=HarvestTask, bind=True, ignore_result=True)
def raw_tweet_harvest(self, topic=None):
    tweet_json = twitter.get_topic_tweets(topic=topic, include_rts=False,
        exclude_replies=True, count=100)

    tweets = []
    for tweet in tweet_json["statuses"]:
        logger.info("Examining tweet: {}".format(tweet))
        if validate_tweet_json(tweet):
            Tweet(
                tweet_id=tweet["id"],
                text=tweet["text"],
                user_screen_name=tweet["user"]["screen_name"],
                user_id=tweet["user"]["id"],
                created=parse_tweet_datetime(tweet["created_at"])
            )

            self.persist_tweet(tweet)

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
