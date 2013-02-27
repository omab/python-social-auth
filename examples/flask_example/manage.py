#!/usr/bin/env python
from flask.ext.script import Server, Manager, Shell
from flask.ext.evolution import Evolution

from example import app, db, models


evolution = Evolution(app)

manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db': db,
    'models': models
}))


@manager.command
def migrate(action):
    # ./manage.py migrate run
    with app.app_context():
        evolution.manager(action)


if __name__ == '__main__':
    manager.run()
