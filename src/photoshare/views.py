from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.view import forbidden_view_config
from pyramid.view import view_config
from .models import DBSession
from .models import User

def users():
    users = DBSession.query(User).all()
    users.sort(key=lambda u: u.name)
    return users


@forbidden_view_config(renderer='templates/login.pt')
def forbidden(request):
    if request.method == 'POST':
        headers = remember(request, int(request.POST['login']))
        response = HTTPFound(request.url)
        response.headerlist.extend(headers)
        return response
    request.response.status_int = 403
    return {'users': users()}


@view_config(route_name='home', renderer='templates/index.pt',
        permission='authenticated')
def app(request):
    return HTTPFound(request.route_url('upload'))


@view_config(route_name='upload', renderer='templates/index.pt',
        request_method='GET', permission='authenticated')
def upload_view(request):
    return {'users': users()}


@view_config(route_name='upload', renderer='json', 
        request_method='POST', permission='authenticated')
def upload(request):
    return {'message': 'ok'}


@view_config(route_name='browse', permission='authenticated',
        renderer='templates/browse.pt')
def browse(request):
    return {'users': users(), 'user': None}


@view_config(route_name='browse-user', permission='authenticated',
        renderer='templates/browse.pt')
def browse_user(request):
    user_id = int(request.matchdict['id'])
    user = DBSession.query(User).get(user_id)
    return {'users': users(), 'user': user, 'photos': []}


@view_config(route_name='api-photos', permission='authenticated',
        renderer='json')
def api_photos(request):
    user_id = int(request.matchdict['id'])
    user = DBSession.query(User).get(user_id)
    return {'photos': repr(user.photos)}
