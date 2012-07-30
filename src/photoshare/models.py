from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import orm
from s4u.sqlalchemy import meta
from s4u.image.model import Image


class User(meta.BaseObject):
    __tablename__ = 'user'
    id = schema.Column(types.Integer(), primary_key=True)
    name = schema.Column(types.UnicodeText(), unique=True)


class Photo(Image):
    exif_date = schema.Column(types.DateTime(timezone=False))
    user_id = schema.Column(types.Integer(),
            schema.ForeignKey('user.id', onupdate='CASCADE',
                ondelete='CASCADE'))
    user = orm.relationship(User,
            backref=orm.backref('photos',
                order_by=[exif_date]))
