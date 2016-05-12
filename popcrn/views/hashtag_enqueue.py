import logging
import os

import json

from popcrn.ingestion.apis.twitter import Twitter
from ConfigParser import SafeConfigParser
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPBadRequest
)

from popcrn.models import (
    RawSession,
    Sentiment
)

from pyramid.response import Response

from popcrn.ingestion import tasks as signatures

from popcrn.sentiment.analyzer import SentimentAnalyzer

from sqlalchemy import create_engine

settings = SafeConfigParser()
settings.read(os.environ.get("POPCRN_INI", "development.ini"))

logger = logging.getLogger(__name__)

twitter = Twitter()
sentiments = SentimentAnalyzer()

@view_config(renderer='json')
def enqueue_topic(request):
    engine = create_engine(settings.get("app:main", "sqlalchemy.url"))
    db = RawSession(bind=engine)
    logger.debug("Connected to the database.")

    topic = request.params.get("topic")
    if not topic:
        message = "No topic provided. Got: {}".format(topic)
        logger.error(message)
        return HTTPBadRequest(message)
    else:
        topic = topic.lower()

    post_body = {
        "topic": topic,
        "is_new": True
    }

    obj = db.query(Sentiment).filter(Sentiment.topic == topic).first()
    if obj:
        logger.info("The topic {} already exists in the database! " +
            "Calculating sentiments...".format(topic))
        post_body["is_new"] = False # an async task is already monitoring this topic
        tweets = [tweet for tweet in obj.tweets]
        logger.info(tweets)
    else:
        logger.info("The topic {} does not exist! Enqueueing new " +
            "database task!".format(topic))
        async_signature = signatures.topic_harvest
        async_signature.delay(topic)

    logger.info("Returning for enqueue topic: {}".format(post_body))
    return Response(json.dumps(post_body))
