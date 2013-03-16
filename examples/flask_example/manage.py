#!/usr/bin/env python
from flask.ext.script import Server, Manager, Shell

from example import app, db, models, Base, engine


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db': db,
    'models': models
}))


@manager.command
def syncdb():
    from example.models import user
    from social.apps.flask_app import models
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    manager.run()
