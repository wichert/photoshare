from sqlalchemy import schema
from sqlalchemy import types
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.orderinglist import ordering_list
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = orm.scoped_session(orm.sessionmaker(
    extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = schema.Column(types.Integer(), primary_key=True)
    name = schema.Column(types.UnicodeText(), unique=True)


class Photo(Base):
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
