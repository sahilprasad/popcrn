import logging

import json
import ast
import os

from popcrn.ingestion.apis.twitter import Twitter
from popcrn.ingestion.tasks import import_user_tweets
from popcrn.util.task_utils import validate_tweet_json, parse_tweet_datetime

from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPBadRequest
)

from popcrn.models import RawSession, Tweet
from popcrn.sentiment.analyzer import SentimentAnalyzer

from pyramid.response import Response

from popcrn.ingestion import tasks as signatures

from sqlalchemy import create_engine

from ConfigParser import SafeConfigParser

logger = logging.getLogger(__name__)

twitter = Twitter()

settings = SafeConfigParser()
settings.read(os.environ.get("POPCRN_INI", "development.ini"))

engine = create_engine(settings.get("app:main", "sqlalchemy.url"))
db = RawSession(bind=engine)

sentiment = SentimentAnalyzer()

@view_config(renderer='json')
def raw_topic_enqueue(request):
    topic = request.params.get("topic")

    if not topic:
        return HTTPBadRequest("A 'topic' parameter is required!")

    topic = topic.lower()

    tweet_json = twitter.get_topic_tweets(topic=topic, include_rts=False,
        exclude_replies=True, count=200)

    tweets = []
    for tweet in tweet_json["statuses"]:
        logger.info("Examining tweet: {}".format(tweet))
        if validate_tweet_json(tweet):
            persist_tweet(tweet, topic)

    result_tweets = []
    db_tweets = db.query(Tweet).filter(Tweet.topic == topic).all()
    for db_tweet in db_tweets:
        result_tweets.append({
            "id": db_tweet.tweet_id,
            "topic": db_tweet.topic,
            "sentiment": db_tweet.sentiment,
            "max_sentiment_word": db_tweet.max_sentiment_word,
            "max_sentiment": db_tweet.max_sentiment_word_value,
            "min_sentiment_word": db_tweet.min_sentiment_word,
            "min_sentiment": db_tweet.min_sentiment_word_value
        })

    return Response(json.dumps(result_tweets))

def persist_tweet(tweet, topic):
    if isinstance(tweet, basestring):
        tweet = json.loads(tweet)
    tweet_id_orig = tweet["id"]
    logger.info("PERSISTING tweet: {}".format(tweet["id"]))
    existing_tweet = db.query(Tweet).filter(Tweet.tweet_id == tweet["id"]).first()
    logger.error("EXISTING TWEET: {}".format(tweet["id"]))
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
            tweet_id=tweet["id"],
            topic=topic,
            text=tweet["text"],
            user_screen_name=tweet["user"]["screen_name"],
            sentiment=avg_sentiment,
            max_sentiment_word=max_sentiment_word,
            max_sentiment_word_value=max_sentiment_word_value,
            min_sentiment_word=min_sentiment_word,
            min_sentiment_word_value=min_sentiment_word_value
        )
        db.add(tweet)
        logger.info("STORING tweet_record: {}".format(tweet.tweet_id))
        db.commit()
    else:
        logger.info("NOT PERSISTING tweet: {}. Already ingested.".format(tweet_id_orig))
