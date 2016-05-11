from oauth2 import (
    Consumer,
    Token,
    Client
)

import logging

logger = logging.getLogger(__name__)


class BaseOAuth(object):
    """
        BaseOAuth is meant to abstract away OAuth2 signing of requests,
        especially in the case of modules that may want to do so for API
        calls.
    """
    def __init__(self, consumer_key=None, consumer_secret=None,
        access_token=None, access_token_secret=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def request(self, url, method="GET", params={}, body='', headers=''):
        if not self.consumer_key or not self.consumer_secret or not self.access_token or not self.access_token_secret:
            message = "BaseOAuth: Required parameters not provided."
            logger.error(message)
            raise Exception(message)

        consumer = Consumer(key=self.consumer_key, secret=self.consumer_secret)
        token = Token(key=self.access_token, secret=self.access_token_secret)
        client = Client(consumer, token)

        _url = url
        if url[-1] != '?':
            _url += '?'

        _url += '&'.join(map(lambda x: "{}={}".format(x, params[x]), params.keys()))
        url = _url
        
        logger.info("{}: {}, Body: {}, Headers: {}".format(method, url, body, headers))
        resp, content = client.request(url, method=method, body=body,
            headers=headers)

        logger.info("Response: {}".format(content))

        return content
