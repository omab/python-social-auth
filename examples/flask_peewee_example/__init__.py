import sys

from flask import Flask, g
from flask.ext import login

sys.path.append('../..')

from social.apps.flask_app.routes import social_auth
from social.apps.flask_app.template_filters import backends
from social.apps.flask_app.peewee.models import *
from peewee import *

# App
app = Flask(__name__)
app.config.from_object('flask_example.settings')

try:
    app.config.from_object('flask_example.local_settings')
except ImportError:
    pass

from models.user import database_proxy, User

# DB
database = SqliteDatabase('test.db')
database_proxy.initialize(database)

app.register_blueprint(social_auth)
init_social(app, database)

login_manager = login.LoginManager()
login_manager.login_view = 'main'
login_manager.login_message = ''
login_manager.init_app(app)

from flask_example import models
from flask_example import routes


@login_manager.user_loader
def load_user(userid):
    try:
        us = User.get(User.id == userid)
        return us
    except User.DoesNotExist:
        pass


@app.before_request
def global_user():
    g.user = login.current_user._get_current_object()


@app.context_processor
def inject_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}


app.context_processor(backends)
