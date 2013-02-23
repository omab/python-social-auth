from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.functional import SimpleLazyObject

try:
    from django.utils.functional import empty as _empty
    empty = _empty
except ImportError:  # django < 1.4
    empty = object()


from social.utils import user_is_authenticated
from social.backends.utils import load_backends
from social.apps.django_app.utils import Storage


class LazyDict(SimpleLazyObject):
    """Lazy dict initialization."""
    def __getitem__(self, name):
        if self._wrapped is empty:
            self._setup()
        return self._wrapped[name]

    def __setitem__(self, name, value):
        if self._wrapped is empty:
            self._setup()
        self._wrapped[name] = value


def backends(request):
    """Load Social Auth current user data to context under the key 'backends'.

    Context entry will have the following keys:
        associated: UserSocialAuth model instances for currently associated
                    accounts
        not_associated: Not associated (yet) backend names
        backends: All backend names.

    If user is not authenticated, then 'associated' list is empty, and there's
    no difference between 'not_associated' and 'backends'.
    """
    def context_value():
        available = load_backends().keys()
        values = {'associated': [],
                  'not_associated': available,
                  'backends': available}
        if user_is_authenticated(request.user):
            associated = Storage.user.get_social_auth_for_user(request.user)
            not_associated = list(set(available) -
                                  set(assoc.provider for assoc in associated))
            values['associated'] = associated
            values['not_associated'] = not_associated
        return values
    return {'backends': LazyDict(context_value)}


def login_redirect(request):
    """Load current redirect to context."""
    value = request.method == 'POST' and \
                request.POST.get(REDIRECT_FIELD_NAME) or \
                request.GET.get(REDIRECT_FIELD_NAME)
    querystring = value and (REDIRECT_FIELD_NAME + '=' + value) or ''
    return {
        'REDIRECT_FIELD_NAME': REDIRECT_FIELD_NAME,
        'REDIRECT_FIELD_VALUE': value,
        'REDIRECT_QUERYSTRING': querystring
    }
