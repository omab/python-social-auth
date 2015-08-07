import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from flask import Flask, g
from flask.ext import login

sys.path.append('../..')

from social.apps.flask_app.routes import social_auth
from social.apps.flask_app.template_filters import backends
from social.apps.flask_app.default.models import init_social

# App
app = Flask(__name__)
app.config.from_object('flask_example.settings')

try:
    app.config.from_object('flask_example.local_settings')
except ImportError:
    pass

# DB
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(Session)

app.register_blueprint(social_auth)
init_social(app, db_session)

login_manager = login.LoginManager()
login_manager.login_view = 'main'
login_manager.login_message = ''
login_manager.init_app(app)

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
    else:
        db_session.rollback()

    db_session.remove()


@app.context_processor
def inject_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}


app.context_processor(backends)
