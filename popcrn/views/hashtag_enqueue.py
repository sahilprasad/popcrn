import logging
import os

import json
import csv

import uuid

from datetime import datetime

from popcrn.ingestion.apis.twitter import Twitter
from ConfigParser import SafeConfigParser
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPBadRequest
)

from popcrn.models import (
    RawSession,
    Sentiment,
    Tweet,
    User
)

from pyramid.response import Response

from popcrn.ingestion import tasks as signatures

from popcrn.sentiment.analyzer import SentimentAnalyzer

from sqlalchemy import create_engine

settings = SafeConfigParser()
settings.read(os.environ.get("POPCRN_INI", "development.ini"))

logger = logging.getLogger(__name__)

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
        "tracked": False
    }

    obj = db.query(Sentiment).filter(Sentiment.topic == topic).first()
    if obj:
        logger.info("The topic {} already exists in the database! " +
            "Calculating sentiments...".format(topic))
        post_body["tracked"] = True # an async task is already monitoring this topic
        alpha3_to_sentiments = {}

        relevant_tweets = db.query(Tweet).filter(Tweet.topic == obj.topic).all()
        for tweet in relevant_tweets:
            logger.error("considering tweet for analysis: {}".format(tweet))
            print "AYE"
            user = db.query(User).filter(User.user_id == tweet.user_id).first()
            if user:
                if alpha3_to_sentiments.get(user.country_code) is None:
                    alpha3_to_sentiments[user.country_code] = []
                alpha3_to_sentiments[user.country_code].append(tweet.sentiment)

        alpha3_to_sentiment_avg = {}
        for country, sents in alpha3_to_sentiments.iteritems():
            sum_of_sentiments = 0
            for country_s in sents:
                sum_of_sentiments += float(country_s)
            country_sentiment = sum_of_sentiments / len(sents)
            alpha3_to_sentiment_avg[country] = country_sentiment

        logger.info(alpha3_to_sentiments)
        logger.info(alpha3_to_sentiment_avg)

        # fix for weird pycountry US/USA non-conversions
        if "US" in alpha3_to_sentiment_avg and "USA" in alpha3_to_sentiment_avg:
            tot_len = 0
            sum_us_sentiments = 0
            for us_sentiment in alpha3_to_sentiments["US"]:
                sum_us_sentiments += float(us_sentiment)
                tot_len += 1
            sum_usa_sentiments = 0
            for usa_sentiment in alpha3_to_sentiments["USA"]:
                sum_usa_sentiments += float(usa_sentiment)
                tot_len += 1
            del alpha3_to_sentiment_avg["US"]
            del alpha3_to_sentiment_avg["USA"]

            alpha3_to_sentiment_avg["USA"] = sum_us_sentiments / tot_len

        post_body["data"] = alpha3_to_sentiment_avg

        csv_uuid = uuid.uuid4()
        print csv_uuid

        csv_link = os.path.join(os.path.dirname(os.path.dirname(__file__)),
            "static", "output", str(csv_uuid) + ".csv")
        print csv_link

        with open(csv_link, "w+") as csv_file:
            fieldnames = ["Country Code", "sentiment"]
            writer = csv.writer(csv_file)
            writer.writerow(fieldnames)

            for country, sentiment_of_country in alpha3_to_sentiment_avg.iteritems():
                writer.writerow([country, sentiment_of_country])

        post_body["csv"] = csv_link
    else:
        sent = Sentiment(created=datetime.now(), topic=topic)
        db.add(sent)
        db.commit()
        logger.info("The topic {} does not exist! Enqueueing new " +
            "database task!".format(topic))
        async_signature = signatures.topic_harvest
        async_signature.delay(topic)

    logger.info("Returning for enqueue topic: {}".format(post_body))
    return Response(json.dumps(post_body))
