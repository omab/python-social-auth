#!/usr/bin/env python
import sys

from flask.ext.script import Server, Manager, Shell

sys.path.append('..')

from flask_me_example import app, db


manager = Manager(app)
manager.add_command('runserver', Server())
manager.add_command('shell', Shell(make_context=lambda: {
    'app': app,
    'db': db
}))


if __name__ == '__main__':
    manager.run()
