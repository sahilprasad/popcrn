import os

from base import BaseOAuth

import logging

import json

import urllib

logger = logging.getLogger(__name__)

API_BASE_URL = "https://api.twitter.com/1.1/{}"

USER_PROFILE_URL = API_BASE_URL.format("users/show.json")
TWEETS_URL = API_BASE_URL.format("statuses/user_timeline.json")
TOPICS_URL = API_BASE_URL.format("search/tweets.json")

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

        for k, v in kwargs.iteritems():
            params[k] = v

        content = self.request(USER_PROFILE_URL, params=params)
        return content

    def get_profile_tweets(self, user_id=None, screen_name=None, **kwargs):
        if not user_id and not screen_name:
            logger.error("Twitter: either user_id or screen_name must be provided.")
            return []

        params = {
            "screen_name": screen_name,
            "user_id": user_id,
        }

        for k, v in kwargs.iteritems():
            params[k] = v

        content = self.request(TWEETS_URL, params=params)
        return json.loads(content)

    def get_topic_tweets(self, topic=None, hashtag=True, **kwargs):
        if not topic:
            logger.error("Twitter: a topic must be provided.")
            return []

        q = topic
        if hashtag and q[0] != "#":
            q = "%23" + q
        q = q.lower()

        params = {
            "q": q
        }

        for k, v in kwargs.iteritems():
            params[k] = v

        content = self.request(TOPICS_URL, params=params)
        return json.loads(content)

    def get_country_code(self, query=None, **kwargs):
        if not query:
            logger.error("Twitter: a query must be provided to search for a geocode.")
            return []

        params = {
            "query": query
        }

        for k, v in kwargs.iteritems():
            params[k] = v

        content = self.request(TOPICS_URL, params=params)
        print content
        return json.loads(content)
