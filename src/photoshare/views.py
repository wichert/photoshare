from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/index.pt')
def my_view(request):
    return {}


@view_config(route_name='upload', request_method='POST', renderer='json')
def upload(request):
    pass
