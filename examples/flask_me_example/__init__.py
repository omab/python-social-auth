import sys

from flask import Flask, g
from flask.ext import login
from flask.ext.mongoengine import MongoEngine

sys.path.append('../..')

from social.apps.flask_app.routes import social_auth
from social.apps.flask_app.me.models import init_social
from social.apps.flask_app.template_filters import backends


# App
app = Flask(__name__)
app.config.from_object('flask_me_example.settings')
app.debug = True

try:
    app.config.from_object('flask_me_example.local_settings')
except ImportError:
    pass

# DB
db = MongoEngine(app)
app.register_blueprint(social_auth)
init_social(app, db)

login_manager = login.LoginManager()
login_manager.login_view = 'main'
login_manager.login_message = ''
login_manager.init_app(app)

from flask_me_example import models
from flask_me_example import routes


@login_manager.user_loader
def load_user(userid):
    try:
        return models.user.User.objects.get(id=userid)
    except (TypeError, ValueError):
        pass


@app.before_request
def global_user():
    g.user = login.current_user


@app.context_processor
def inject_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}


app.context_processor(backends)
