import logging
import os

from popcrn.ingestion.apis.twitter import Twitter
from ConfigParser import SafeConfigParser
from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPBadRequest
)

from pyramid.response import Response

from popcrn.ingestion import tasks as signatures

settings = SafeConfigParser()
settings.read(os.environ.get("POPCRN_INI", "development.ini"))

logger = logging.getLogger(__name__)

twitter = Twitter()

@view_config(renderer='json')
def enqueue_topic(request):
    engine = create_engine(settings.get("app:main", "sqlalchemy.url"))
    db = RawSession(bind=engine)
    logger.debug("Connected to the database.")

    topic = request.params.get("topic")
    if not topic:
        return HTTPBadRequest("No topic provided. Got: {}".format(topic))
    else:
        topic = topic.lower()

    post_body = {
        "topic": topic.lower(),
        "is_new": True
    }

    obj = db.query(Sentiment).filter_by(Sentiment.topic == topic.lower()).all()
    if obj:
        # TODO: produce a sentiment mapping to be sent back in the "data" key
        pass
    else:
        post_body["is_new"] = False
        async_signature = signatures.topic_harvest
        async_signature.delay(topic)

    return body
