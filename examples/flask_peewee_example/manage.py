#!/usr/bin/env python
import sys

from flask.ext.script import Server, Manager, Shell

sys.path.append('..')

from flask_example import app, database


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app
}))


@manager.command
def syncdb():
    from flask_example.models.user import User
    from social.apps.flask_app.peewee.models import FlaskStorage

    database.create_tables([User, FlaskStorage.user, FlaskStorage.nonce, FlaskStorage.association, FlaskStorage.code])

if __name__ == '__main__':
    manager.run()
