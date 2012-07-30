# vi: fileencoding=utf-8
from s4u.upgrade import upgrade_step
from s4u.sqlalchemy import meta
from models import User


@upgrade_step(require=['sql'])
def add_missing_entities(environment):
    engine = environment['sql-engine']
    meta.metadata.create_all(engine)


@upgrade_step(require=['sql'])
def add_initial_users(environment):
    session = meta.Session()
    session.add(User(name=u'Åse'))
    session.add(User(name=u'Claude'))
    session.add(User(name=u'Erin'))
    session.add(User(name=u'Fleur'))
    session.add(User(name=u'Gustavo'))
    session.add(User(name=u'Helena'))
    session.add(User(name=u'Karl-Heinz'))
    session.add(User(name=u'Lando'))
    session.add(User(name=u'Linn'))
    session.add(User(name=u'Marjolein'))
    session.add(User(name=u'Panikos'))
    session.add(User(name=u'Rakel'))
    session.add(User(name=u'Wichert'))
