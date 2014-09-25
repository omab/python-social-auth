from django.conf import settings
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST

from social.utils import setting_name
from social.actions import do_auth, do_complete, do_disconnect
from social.apps.django_app.utils import psa


NAMESPACE = getattr(settings, setting_name('URL_NAMESPACE'), None) or 'social'


@psa('{0}:complete'.format(NAMESPACE))
def auth(request, backend):
    return do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)


@csrf_exempt
@psa('{0}:complete'.format(NAMESPACE))
def complete(request, backend, *args, **kwargs):
    """Authentication complete view"""
    return do_complete(request.backend, _do_login, request.user,
                       redirect_name=REDIRECT_FIELD_NAME, *args, **kwargs)


@login_required
@psa()
@require_POST
@csrf_protect
def disconnect(request, backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    return do_disconnect(request.backend, request.user, association_id,
                         redirect_name=REDIRECT_FIELD_NAME)


def _do_login(backend, user, social_user):
    user.backend = '{0}.{1}'.format(backend.__module__,
                                  backend.__class__.__name__)
    login(backend.strategy.request, user)
    if backend.setting('SESSION_EXPIRATION', False):
        # Set session expiration date if present and enabled
        # by setting. Use last social-auth instance for current
        # provider, users can associate several accounts with
        # a same provider.
        expiration = social_user.expiration_datetime()
        if expiration:
            try:
                backend.strategy.request.session.set_expiry(
                    expiration.seconds + expiration.days * 86400
                )
            except OverflowError:
                # Handle django time zone overflow
                backend.strategy.request.session.set_expiry(None)
