from django.contrib.auth import login, REDIRECT_FIELD_NAME, BACKEND_SESSION_KEY
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST

from social.actions import do_auth, do_complete, do_disconnect
from social.apps.django_app.utils import strategy, setting, BackendWrapper


DEFAULT_REDIRECT = setting('LOGIN_REDIRECT_URL')
LOGIN_ERROR_URL = setting('LOGIN_ERROR_URL', setting('LOGIN_URL'))


@strategy('social:complete')
def auth(request, backend):
    return do_auth(request.strategy, redirect_name=REDIRECT_FIELD_NAME)


@csrf_exempt
@strategy('social:complete')
def complete(request, backend, *args, **kwargs):
    """Authentication complete view, override this view if transaction
    management doesn't suit your needs."""
    return do_complete(request.strategy, _do_login, request.user,
                       redirect_name=REDIRECT_FIELD_NAME, *args, **kwargs)


@login_required
@strategy()
@require_POST
@csrf_protect
def disconnect(request, backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    return do_disconnect(request.strategy, request.user, association_id,
                         redirect_name=REDIRECT_FIELD_NAME)


def _do_login(strategy, user):
    login(strategy.request, user)
    strategy.session_set('original_' + BACKEND_SESSION_KEY,
                         strategy.session_get(BACKEND_SESSION_KEY))
    strategy.session_set(BACKEND_SESSION_KEY, '%s.%s' % (
        BackendWrapper.__module__,
        BackendWrapper.__name__
    ))
    # user.social_user is the used UserSocialAuth instance defined in
    # authenticate process
    social_user = user.social_user
    if strategy.setting('SESSION_EXPIRATION', True):
        # Set session expiration date if present and not disabled
        # by setting. Use last social-auth instance for current
        # provider, users can associate several accounts with
        # a same provider.
        expiration = social_user.expiration_datetime()
        if expiration:
            try:
                strategy.request.session.set_expiry(expiration)
            except OverflowError:
                # Handle django time zone overflow
                strategy.request.session.set_expiry(None)
