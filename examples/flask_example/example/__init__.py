import sys

from sqlalchemy import create_engine

from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import login


sys.path.append('../..')

from social.apps.fl.routes import social_auth
from social.apps.fl.models import init_social

# App
app = Flask(__name__)
app.config.from_object('example.settings')
app.config.from_object('example.local_settings')

# DB
db = SQLAlchemy(app)
db.metadata.bind = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

app.register_blueprint(social_auth)
social_storage = init_social(app, db)

login_manager = login.LoginManager()
login_manager.login_view = 'main'
login_manager.login_message = ''
login_manager.setup_app(app)

from example import models
from example import routes


@login_manager.user_loader
def load_user(userid):
    try:
        return models.user.User.query.get(int(userid))
    except (TypeError, ValueError):
        pass


@app.before_request
def global_user():
    g.user = login.current_user


@app.teardown_appcontext
def commit_on_success(error=None):
    if error is None:
        db.session.commit()


@app.context_processor
def inject_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}
