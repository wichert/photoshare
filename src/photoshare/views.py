import datetime
from cStringIO import StringIO
import zipfile
from pyramid.httpexceptions import HTTPFound
from pyramid.security import authenticated_userid
from pyramid.security import remember
from pyramid.view import forbidden_view_config
from pyramid.view import view_config
from s4u.sqlalchemy import meta
import PIL.Image
from .models import User
from .models import Photo

def users():
    users = meta.Session.query(User).all()
    users.sort(key=lambda u: u.name)
    return users


def photo_info(request, photo):
    static_url = request.static_url
    return {'download': static_url(photo.filesystem_path),
            'thumbnail': static_url(photo.scale(width=260, height=180, crop=True).filesystem_path),
            'date': photo.exif_date.strftime('%m %B %Y at %H:%M') if photo.exif_date else None,
            'user': photo.user.name}


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
    upload = request.POST['file']
    user_id = authenticated_userid(request)
    user = meta.Session.query(User).get(user_id)
    photo = Photo(upload.file.read(), upload.filename)
    user.photos.append(photo)
    upload.file.seek(0)
    img = PIL.Image.open(upload.file)
    if hasattr(img, '_getexif'):
        tags = img._getexif() or {}
        for date_tag in [36867, 36868, 306]:  # Possible timestamps
            value = tags.get(date_tag)
            if value is not None:
                photo.exif_date = datetime.datetime.strptime(
                        value, '%Y:%m:%d %H:%M:%S')
                break
    return {'message': 'ok'}


@view_config(route_name='browse', permission='authenticated',
        renderer='templates/browse.pt')
def browse(request):
    query = meta.Session.query(Photo).order_by(Photo.id.desc()).limit(12)
    photos = [photo_info(request, photo) for photo in query]
    return {'users': users(), 'user': None, 'photos': photos}


@view_config(route_name='browse-user', context=User,
        permission='authenticated', renderer='templates/browse.pt')
def browse_user(context, request):
    photos = [photo_info(request, photo) for photo in context.photos]
    return {'users': users(), 'user': context, 'photos': photos}


@view_config(route_name='download-user', permission='authenticated')
def download_user(context, request):
    output = StringIO()
    zip = zipfile.ZipFile(output, 'w', zipfile.ZIP_STORED)
    for photo in context.photos:
        zip.write(photo.filesystem_path)
    zip.close()
    output.seek(0)
    response = request.response
    response.content_disposition = 'attachment; filename=%s.zip' % \
            context.name.encode('utf8')
    response.body_file = output
    return response
