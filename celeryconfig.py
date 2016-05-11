from kombu import Queue

import os

_BROKER_USER = os.environ.get('BROKER_USER', os.environ.get('ENV_BROKER_USER', 'guest'))
_BROKER_PASSWORD = os.environ.get('BROKER_PASSWORD', os.environ.get('ENV_BROKER_PASSWORD', 'guest'))
_BROKER_HOST = os.environ.get('BROKER_HOST', os.environ.get('ENV_BROKER_HOST', 'localhost'))
_BROKER_PORT = int(os.environ.get('BROKER_PORT', os.environ.get('ENV_BROKER_PORT', 5672)))

BROKER_URL = u'amqp://{user}:{password}@{host}:{port}/'.format(
    user=_BROKER_USER,
    password=_BROKER_PASSWORD,
    host=_BROKER_HOST,
    port=_BROKER_PORT,
)

CELERY_ACCEPT_CONTENT = ['json', 'msgpack']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = None

CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_SEND_EVENTS = True
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_TASK_PUBLISH_RETRY = True

CELERY_ALWAYS_EAGER = False
if os.environ.get('CELERY_ALWAYS_EAGER'):
    CELERY_ALWAYS_EAGER = True
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

CELERY_TIMEZONE = 'UTC'

CELERY_DEFAULT_QUEUE = 'celery'

CELERY_QUEUES = [
    Queue('celery', routing_key='celery'),
    Queue('twitteruser', routing_key='userimport'),
    Queue('tweet', routing_key='tweetimport')
]

CELERY_ROUTES = {
    'popcrn.ingestion.tasks.import_user_tweets': {
        'queue': 'userimport'
    },
    'popcrn.ingestion.tasks.import_tweets': {
        'queue': 'tweetimport'
    }
}

CELERYBEAT_SCHEDULE = {

}
