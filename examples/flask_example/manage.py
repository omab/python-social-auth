#!/usr/bin/env python
import sys

from flask.ext.script import Server, Manager, Shell

sys.path.append('..')

from flask_example import app, db, models, Base, engine


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db': db,
    'models': models
}))


@manager.command
def syncdb():
    from flask_example.models import user
    from social.apps.flask_app import models
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    manager.run()
