from popcrn.celeryapp import (
    app,
    HarvestTask
)

from popcrn.models import Tweet
from popcrn.util.task_utils import (
    parse_tweet_datetime,
    validate_tweet_json
)

from popcrn.ingestion.apis.twitter import Twitter

import logging

logger = logging.getLogger(__name__)

twitter = Twitter()

@app.task(base=HarvestTask, bind=True, ignore_result=True, rate_limit='5/m')
def import_user_tweets(self, user_id=None, screen_name=None, **kwargs):
    tweet_json = twitter.get_user_tweets(user_id=user_id, screen_name=screen_name,
        **kwargs)
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
