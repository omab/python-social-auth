from flask import g, request

from social.utils import user_backends_data
from social.apps.flask_app.utils import get_helper


def backends(request):
    """Load Social Auth current user data to context under the key 'backends'.
    Will return the output of social.utils.user_backends_data."""
    return {'backends': user_backends_data(g.user, get_helper('STORAGE'))}


def login_redirect():
    """Load current redirect to context."""
    value = request.form.get('next', '') or \
            request.args.get('next', '')
    return {
        'REDIRECT_FIELD_NAME': 'next',
        'REDIRECT_FIELD_VALUE': value,
        'REDIRECT_QUERYSTRING': value and ('next=' + value) or ''
    }
