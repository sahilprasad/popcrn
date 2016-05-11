import logging

from popcrn.ingestion.apis.twitter import Twitter
from popcrn.ingestion.tasks import import_user_tweets

from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPBadRequest
)

from pyramid.response import Response

logger = logging.getLogger(__name__)

twitter = Twitter()

@view_config(renderer='json')
def root_view(request):
    user_id = request.params.get("user_id")
    screen_name = request.params.get("screen_name")

    if not user_id and not screen_name:
        logger.info("BAD REQUEST: {}".format(request))
        logger.info(request.params)
        return HTTPBadRequest()

    tweet_json = twitter.get_profile_tweets(user_id=user_id, screen_name=screen_name,
        include_rts=False, exclude_replies=True, count=50)
    for i in tweet_json:
        print
        print i
        print
    
    import_user_tweets.persist_tweets_json(tweet_json)
    tweets = import_user_tweets.get_tweets_of_user(user_id=user_id, screen_name=screen_name)

    return Response(tweets)
