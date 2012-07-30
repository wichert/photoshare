from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import orm
from sqlalchemy.ext.orderinglist import ordering_list
from s4u.sqlalchemy import meta


class User(meta.BaseObject):
    __tablename__ = 'user'
    id = schema.Column(types.Integer(), primary_key=True)
    name = schema.Column(types.UnicodeText(), unique=True)


class Photo(meta.BaseObject):
    __tablename__ = 'photo'

    id = schema.Column(types.Integer(), primary_key=True)
    user_id = schema.Column(types.Integer(),
            schema.ForeignKey('user.id', onupdate='CASCADE',
                ondelete='CASCADE'))
    position = schema.Column(types.Integer())
    user = orm.relationship(User,
            backref=orm.backref('photos',
                collection_class=ordering_list('position'),
                order_by=[position]))
