from pyramid.config import Configurator
from pyramid.security import Allow
from pyramid.security import Authenticated
from sqlalchemy import engine_from_config
from .models import DBSession


class DefaultRoot(object):
    __acl__ = [(Allow, Authenticated, 'authenticated')]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    config = Configurator(settings=settings)
    config.set_root_factory(DefaultRoot)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('upload', '/upload')
    config.add_route('browse', '/browse')
    config.add_route('browse-user', '/browse/{id:\d+}')
    config.add_route('api-photos', '/api/photos/{id:\d+}')
    config.scan()
    return config.make_wsgi_app()
