from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from models import (
    DBSession,
    Base,
)

from views.root import root_view
from views.hashtag_enqueue import enqueue_topic
from views.raw_topic_enqueue import raw_topic_enqueue
from views.country_sentiment import country_sentiment

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('tweets', '/tweets')
    config.add_view(root_view, 'tweets')
    config.add_route('topic', '/topic')
    config.add_view(enqueue_topic, 'topic')
    config.add_route('raw_topic', '/raw_topic')
    config.add_view(raw_topic_enqueue, 'raw_topic')
    config.add_route('country', '/country')
    config.add_view(country_sentiment, 'country')
    # config.scan()
    return config.make_wsgi_app()
