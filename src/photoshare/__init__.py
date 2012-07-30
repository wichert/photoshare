from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow
from pyramid.security import Authenticated
from s4u.sqlalchemy import meta
from .models import User


class DefaultRoot(object):
    __acl__ = [(Allow, Authenticated, 'authenticated')]

    def __init__(self, request):
        pass


def user_factory(request):
    user_id = int(request.matchdict['id'])
    return meta.Session.query(User).get(user_id)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('s4u.sqlalchemy')
    config.include('s4u.image')
    config.set_root_factory(DefaultRoot)
    config.set_authentication_policy(
            AuthTktAuthenticationPolicy('photoshare',
                include_ip=False,
                max_age=60 * 60 * 24 * 7,
                timeout=60 * 60 * 24 * 7,
                reissue_time=60 * 60 * 24,
                http_only=True))
    config.set_authorization_policy(
            ACLAuthorizationPolicy())
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('upload', '/upload')
    config.add_route('browse', '/browse')
    config.add_route('browse-user', '/browse/{id:\d+}',
            factory=user_factory)
    config.add_route('download-user', '/browse/{id:\d+}/download',
            factory=user_factory)
    config.scan()
    return config.make_wsgi_app()
