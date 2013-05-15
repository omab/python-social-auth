import sys

from sqlalchemy import create_engine

from flask import Flask, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import login

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


sys.path.append('../..')

from social.apps.flask_app.routes import social_auth
from social.apps.flask_app.models import init_social
from social.apps.flask_app.template_filters import backends

# App
app = Flask(__name__)
app.config.from_object('flask_example.settings')

try:
    app.config.from_object('flask_example.local_settings')
except ImportError:
    pass

# DB
db = SQLAlchemy(app)
db.metadata.bind = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                       convert_unicode=True)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

app.register_blueprint(social_auth)
social_storage = init_social(app, Base)

login_manager = login.LoginManager()
login_manager.login_view = 'main'
login_manager.login_message = ''
login_manager.setup_app(app)

from flask_example import models
from flask_example import routes


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
        db_session.commit()


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


@app.context_processor
def inject_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}


app.context_processor(backends)
