#!/usr/bin/env python
import sys

from flask.ext.script import Server, Manager, Shell

sys.path.append('..')

from flask_example import app, db


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db': db
}))


@manager.command
def syncdb():
    from flask_example.models import user
    from social.apps.flask_app import models
    db.drop_all()
    db.create_all()

if __name__ == '__main__':
    manager.run()
