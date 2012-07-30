# vi: fileencoding=utf-8
import os
import sys
import transaction
from sqlalchemy import engine_from_config
from pyramid.paster import get_appsettings
from pyramid.paster import setup_logging
from s4u.sqlalchemy import init_sqlalchemy
from s4u.sqlalchemy import meta
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
    init_sqlalchemy(engine)
    meta.Session.metadata.create_all(engine)
    with transaction.manager:
        meta.Session.add(User(name=u'Åse'))
        meta.Session.add(User(name=u'Claude'))
        meta.Session.add(User(name=u'Erin'))
        meta.Session.add(User(name=u'Fleur'))
        meta.Session.add(User(name=u'Gustavo'))
        meta.Session.add(User(name=u'Helena'))
        meta.Session.add(User(name=u'Karl-Heinz'))
        meta.Session.add(User(name=u'Lando'))
        meta.Session.add(User(name=u'Linn'))
        meta.Session.add(User(name=u'Marjolein'))
        meta.Session.add(User(name=u'Panikos'))
        meta.Session.add(User(name=u'Rakel'))
        meta.Session.add(User(name=u'Wichert'))
