from urllib2 import quote

from flask import g, request, session, Response, redirect, Blueprint
from flask.ext.login import login_required, login_user

from social.utils import sanitize_redirect, user_is_authenticated
from social.apps.flask_app.utils import strategy


social_auth = Blueprint('social', __name__)


@social_auth.route('/login/<string:backend>/', methods=['GET', 'POST'])
@strategy('social.complete')
def auth(backend):
    # Save any defined next value into session
    strategy = g.strategy
    data = request.form if request.method == 'POST' else request.args
    if 'next' in data:
        # Check and sanitize a user-defined GET/POST next field value
        redirect_uri = data['next']
        if strategy.setting('SANITIZE_REDIRECTS', True):
            redirect_uri = sanitize_redirect(request.host, redirect_uri)
        session['next'] = redirect_uri or \
                          strategy.setting('LOGIN_REDIRECT_URL')
    return strategy.start()


@social_auth.route('/complete/<string:backend>/', methods=['GET', 'POST'])
@strategy('social.complete')
def complete(backend, *args, **kwargs):
    """Authentication complete view, override this view if transaction
    management doesn't suit your needs."""
    strategy = g.strategy
    # pop redirect value before the session is trashed on login()
    redirect_value = session.get('next', '') or \
                     request.form.get('next', '') or \
                     request.args.get('next', '')

    is_authenticated = user_is_authenticated(g.user)
    user = is_authenticated and g.user or None
    url = strategy.setting('LOGIN_REDIRECT_URL')

    if session.get('partial_pipeline'):
        data = session.pop('partial_pipeline')
        kwargs = kwargs.copy()
        kwargs.setdefault('user', user)
        idx, xargs, xkwargs = strategy.from_session(data, request=request,
                                                    *args, **kwargs)

        if xkwargs.get('backend', '') == backend:
            user = strategy.continue_pipeline(pipeline_index=idx,
                                              *xargs, **xkwargs)
        else:
            strategy.clean_partial_pipeline()
            user = strategy.complete(user=user, request=request,
                                     *args, **kwargs)
    else:
        user = strategy.complete(user=user, request=request,
                                 *args, **kwargs)

    if isinstance(user, Response):
        return user

    if is_authenticated:
        if not user:
            url = redirect_value or strategy.setting('LOGIN_REDIRECT_URL')
        else:
            url = redirect_value or \
                  strategy.setting('NEW_ASSOCIATION_REDIRECT_URL') or \
                  strategy.setting('LOGIN_REDIRECT_URL')
    elif user:
        if getattr(user, 'is_active', True):
            # catch is_new flag before login() resets the instance
            is_new = getattr(user, 'is_new', False)
            login_user(user)
            # user.social_user is the used UserSocialAuth instance defined
            # in authenticate process
            social_user = user.social_user
            # store last login backend name in session
            session['social_auth_last_login_backend'] = social_user.provider

            # Remove possible redirect URL from session, if this is a new
            # account, send him to the new-users-page if defined.
            new_user_redirect = strategy.setting('NEW_USER_REDIRECT_URL')
            if new_user_redirect and is_new:
                url = new_user_redirect
            else:
                url = redirect_value or strategy.setting('LOGIN_REDIRECT_URL')
        else:
            url = strategy.setting('INACTIVE_USER_URL') or \
                  strategy.setting('LOGIN_ERROR_URL') or \
                  strategy.setting('LOGIN_URL')
    else:
        url = strategy.setting('LOGIN_ERROR_URL') or \
              strategy.setting('LOGIN_URL')

    if redirect_value and redirect_value != url:
        redirect_value = quote(redirect_value)
        url += ('?' in url and '&' or '?') + \
               '%s=%s' % ('next', redirect_value)
    return redirect(url)


@social_auth.route('/disconnect/<string:backend>/', methods=['GET', 'POST'])
@social_auth.route('/disconnect/<string:backend>/<int:association_id>/',
                   methods=['GET', 'POST'])
@login_required
@strategy()
#@disconnect_view
def disconnect(backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    strategy = g.strategy
    strategy.disconnect(g.user, association_id)
    url = request.form.get('next', '') or \
          request.args.get('next', '') or \
          strategy.setting('DISCONNECT_REDIRECT_URL') or \
          strategy.setting('LOGIN_REDIRECT_URL')
    return redirect(url)
