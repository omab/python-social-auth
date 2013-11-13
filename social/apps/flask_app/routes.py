from flask import g, Blueprint, request
from flask.ext.login import login_required, login_user

from social.actions import do_auth, do_complete, do_disconnect
from social.apps.flask_app.utils import strategy


social_auth = Blueprint('social', __name__)


@social_auth.route('/login/<string:backend>/', methods=('GET', 'POST'))
@strategy('social.complete')
def auth(backend):
    return do_auth(g.strategy)


@social_auth.route('/complete/<string:backend>/', methods=('GET', 'POST'))
@strategy('social.complete')
def complete(backend, *args, **kwargs):
    """Authentication complete view, override this view if transaction
    management doesn't suit your needs."""
    return do_complete(g.strategy, login=do_login, user=g.user,
                       *args, **kwargs)


@social_auth.route('/disconnect/<string:backend>/', methods=('POST',))
@social_auth.route('/disconnect/<string:backend>/<int:association_id>/',
                   methods=('POST',))
@login_required
@strategy()
def disconnect(backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    return do_disconnect(g.strategy, g.user, association_id)


def do_login(strategy, user):
    return login_user(user, remember=request.cookies.get('remember') or
                                     request.args.get('remember') or
                                     request.form.get('remember') or False)
