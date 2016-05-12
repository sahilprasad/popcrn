import logging

import json
import ast

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
        logger.error("BAD REQUEST: {}".format(request))
        logger.error("PARAMS: {}".format(request.params))
        return HTTPBadRequest("Invalid request parameters provided. One of 'user_id' or 'screen_name' must be provided.")

    result = twitter.get_profile_tweets(user_id=user_id, screen_name=screen_name)
    return Response(json.dumps(result))
