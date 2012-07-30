from pyramid.security import Allow
from pyramid.security import Authenticated
from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import orm
from s4u.sqlalchemy import meta
from s4u.image.model import Image


class User(meta.BaseObject):
    __tablename__ = 'user'
    id = schema.Column(types.Integer(), primary_key=True)
    name = schema.Column(types.UnicodeText(), unique=True)

    @orm.reconstructor
    def _reconstruct(self):
        self.__acl__ = [
                (Allow, Authenticated, 'authenticated'),
                (Allow, self.id, 'edit'),
                ]

class Photo(Image):
    exif_date = schema.Column(types.DateTime(timezone=False))
    user_id = schema.Column(types.Integer(),
            schema.ForeignKey('user.id', onupdate='CASCADE',
                ondelete='CASCADE'))
    user = orm.relationship(User,
            backref=orm.backref('photos',
                order_by=[exif_date]))

    @orm.reconstructor
    def _reconstruct(self):
        self.__acl__ = [
                (Allow, Authenticated, 'authenticated'),
                (Allow, self.user_id, ['edit', 'delete']),
                ]
