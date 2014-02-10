import os
import sys

sys.path.append('../..')

from sqlalchemy import engine_from_config

from pyramid.paster import get_appsettings, setup_logging
from pyramid.scripts.common import parse_vars

from social.apps.pyramid_app.models import init_social

from example.models import DBSession, Base
from example.settings import SOCIAL_AUTH_SETTINGS


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    init_social(SOCIAL_AUTH_SETTINGS, Base, DBSession)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
