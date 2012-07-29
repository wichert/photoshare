import os
import sys
import transaction
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings
from pyramid.paster import setup_logging
from ..models import DBSession
from ..models import Base
from ..models import User


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd)) 
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        DBSession.add(User(name=u'Åse'))
        DBSession.add(User(name=u'Claude'))
        DBSession.add(User(name=u'Erin'))
        DBSession.add(User(name=u'Fleur'))
        DBSession.add(User(name=u'Gustavo'))
        DBSession.add(User(name=u'Helena'))
        DBSession.add(User(name=u'Karl-Heinz'))
        DBSession.add(User(name=u'Lando'))
        DBSession.add(User(name=u'Linn'))
        DBSession.add(User(name=u'Marjolein'))
        DBSession.add(User(name=u'Panikos'))
        DBSession.add(User(name=u'Rakel'))
        DBSession.add(User(name=u'Wichert'))
