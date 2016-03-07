import os

from base import BaseOAuth

import logging

logger = logging.getLogger(__name__)

API_BASE_URL = "https://api.twitter.com/1.1/{}"
USER_PROFILE_URL = API_BASE_URL.format("users/show.json")

env = os.environ

class Twitter(BaseOAuth):
    def __init__(self):
        super(Twitter, self).__init__(
            consumer_key=env.get('TWITTER_CONSUMER_KEY'),
            consumer_secret=env.get('TWITTER_CONSUMER_SECRET'),
            access_token=env.get('TWITTER_ACCESS_TOKEN'),
            access_token_secret=env.get('TWITTER_ACCESS_SECRET')
        )

    def get_profile(self, screen_name=None, user_id=None, **kwargs):
        if not user_name and not user_id:
            logger.error("Twitter: neither screen_name nor user_id was provided.")
            return []

        params = {
            "screen_name": screen_name,
            "user_id": user_id,
        }

        for k, v in kwargs:
            params[k] = v

        content = self.request(USER_PROFILE_URL, params=params)
        return content

    def get_profile_tweets(self, user_id=None):
        if not user_id:
            logger.error("Twitter: user_id not provided.")
            return []

        # TODO: implement tweet retrieval
