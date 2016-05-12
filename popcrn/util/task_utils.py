import logging

from datetime import datetime

logger = logging.getLogger(__name__)

def validate_tweet_json(tweet):
    if not tweet.get("id"):
        logger.info("Tweet has no id: {}".format(tweet))
    elif not tweet.get("text"):
        logger.info("Tweet has no text: {}".format(tweet))
    elif not tweet.get("user"):
        logger.info("Tweet has no user information: {}".format(tweet))
    elif not tweet["user"].get("id"):
        logger.info("Tweet's user information does not have an id: {}".format(tweet))
    elif not tweet["user"].get("screen_name"):
        logger.info("Tweet's user information does not have a screen_name: {}".format(tweet))
    else:
        return True

    return False

def parse_tweet_datetime(tweet_datetime):
    """
        Returns a Datetime object given a typical datetime string given by the
        Twitter API.

        Ex. Mon Mar 21 23:15:39 +0000 2016
    """

    dt = datetime.strptime(tweet_datetime, '%a %b %d %H:%M:%S +0000 %Y')
    return dt
