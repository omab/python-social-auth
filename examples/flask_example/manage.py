#!/usr/bin/env python
import sys

from flask.ext.script import Server, Manager, Shell

sys.path.append('..')

from flask_example import app, db_session, engine


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db_session': db_session
}))


@manager.command
def syncdb():
    from flask_example.models import user
    from social.apps.flask_app.default import models
    user.Base.metadata.create_all(engine)
    models.PSABase.metadata.create_all(engine)

if __name__ == '__main__':
    manager.run()
