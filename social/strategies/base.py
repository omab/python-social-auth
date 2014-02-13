import time
import random
import hashlib

import six

from social.utils import setting_name, module_member
from social.store import OpenIdStore, OpenIdSessionWrapper
from social.pipeline import DEFAULT_AUTH_PIPELINE, DEFAULT_DISCONNECT_PIPELINE


class BaseTemplateStrategy(object):
    def __init__(self, strategy):
        self.strategy = strategy

    def render(self, tpl=None, html=None, context=None):
        if not tpl and not html:
            raise ValueError('Missing template or html parameters')
        context = context or {}
        if tpl:
            return self.render_template(tpl, context)
        else:
            return self.render_string(html, context)

    def render_template(self, tpl, context):
        raise NotImplementedError('Implement in subclass')

    def render_string(self, html, context):
        raise NotImplementedError('Implement in subclass')


class BaseStrategy(object):
    ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyz' \
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                    '0123456789'

    def __init__(self, backend=None, storage=None, request=None,
                 tpl=BaseTemplateStrategy, backends=None, *args, **kwargs):
        self.tpl = tpl(self)
        self.request = request
        self.storage = storage
        self.backends = backends
        self.backend = backend(strategy=self, *args, **kwargs) \
                            if backend else None

    def setting(self, name, default=None, backend=None):
        names = [setting_name(name), name]
        backend = backend or getattr(self, 'backend', None)
        if backend:
            names.insert(0, setting_name(backend.name, name))
        for name in names:
            try:
                return self.get_setting(name)
            except (AttributeError, KeyError):
                pass
        return default

    def start(self):
        # Clean any partial pipeline info before starting the process
        self.clean_partial_pipeline()
        if self.backend.uses_redirect():
            return self.redirect(self.backend.auth_url())
        else:
            return self.html(self.backend.auth_html())

    def complete(self, *args, **kwargs):
        return self.backend.auth_complete(*args, **kwargs)

    def continue_pipeline(self, *args, **kwargs):
        return self.backend.continue_pipeline(*args, **kwargs)

    def disconnect(self, user, association_id=None, *args, **kwargs):
        return self.backend.disconnect(
            user=user, association_id=association_id,
            *args, **kwargs
        )

    def authenticate(self, *args, **kwargs):
        kwargs['strategy'] = self
        kwargs['storage'] = self.storage
        kwargs['backend'] = self.backend
        return self.backend.authenticate(*args, **kwargs)

    def create_user(self, *args, **kwargs):
        return self.storage.user.create_user(*args, **kwargs)

    def get_user(self, *args, **kwargs):
        return self.storage.user.get_user(*args, **kwargs)

    def session_setdefault(self, name, value):
        self.session_set(name, value)
        return self.session_get(name)

    def openid_session_dict(self, name):
        # Many frameworks are switching the session serialization from Pickle
        # to JSON to avoid code execution risks. Flask did this from Flask
        # 0.10, Django is switching to JSON by default from version 1.6.
        #
        # Sadly python-openid stores classes instances in the session which
        # fails the JSON serialization, the classes are:
        #
        #   openid.yadis.manager.YadisServiceManager
        #   openid.consumer.discover.OpenIDServiceEndpoint
        #
        # This method will return a wrapper over the session value used with
        # openid (a dict) which will automatically keep a pickled value for the
        # mentioned classes.
        return OpenIdSessionWrapper(self.session_setdefault(name, {}))

    def to_session_value(self, val):
        return val

    def from_session_value(self, val):
        return val

    def partial_to_session(self, next, backend, request=None, *args, **kwargs):
        user = kwargs.get('user')
        social = kwargs.get('social')
        clean_kwargs = {
            'response': kwargs.get('response') or {},
            'details': kwargs.get('details') or {},
            'username': kwargs.get('username'),
            'uid': kwargs.get('uid'),
            'is_new': kwargs.get('is_new') or False,
            'new_association': kwargs.get('new_association') or False,
            'user': user and user.id or None,
            'social': social and {
                'provider': social.provider,
                'uid': social.uid
            } or None
        }
        # Only allow well-known serializable types
        types = (dict, list, tuple, set) + six.integer_types + \
                six.string_types + (six.text_type,) + (six.binary_type,)
        clean_kwargs.update((name, value) for name, value in kwargs.items()
                                if isinstance(value, types))
        # Clean any MergeDict data type from the values
        clean_kwargs.update((name, dict(value))
                                for name, value in clean_kwargs.items()
                                    if isinstance(value, dict))
        return {
            'next': next,
            'backend': backend.name,
            'args': tuple(map(self.to_session_value, args)),
            'kwargs': dict((key, self.to_session_value(val))
                                for key, val in clean_kwargs.items())
        }

    def partial_from_session(self, session):
        kwargs = session['kwargs'].copy()
        user = kwargs.get('user')
        social = kwargs.get('social')
        if isinstance(social, dict):
            kwargs['social'] = self.storage.user.get_social_auth(**social)
        if user:
            kwargs['user'] = self.storage.user.get_user(user)
        return (
            session['next'],
            session['backend'],
            list(map(self.from_session_value, session['args'])),
            dict((key, self.from_session_value(val))
                    for key, val in kwargs.items())
        )

    def clean_partial_pipeline(self, name='partial_pipeline'):
        self.session_pop(name)

    def openid_store(self):
        return OpenIdStore(self)

    def get_pipeline(self):
        return self.setting('PIPELINE', DEFAULT_AUTH_PIPELINE)

    def get_disconnect_pipeline(self):
        return self.setting('DISCONNECT_PIPELINE', DEFAULT_DISCONNECT_PIPELINE)

    def random_string(self, length=12, chars=ALLOWED_CHARS):
        # Implementation borrowed from django 1.4
        try:
            random.SystemRandom()
        except NotImplementedError:
            key = self.setting('SECRET_KEY', '')
            seed = '{0}{1}{2}'.format(random.getstate(), time.time(), key)
            random.seed(hashlib.sha256(seed.encode()).digest())
        return ''.join([random.choice(chars) for i in range(length)])

    def absolute_uri(self, path=None):
        uri = self.build_absolute_uri(path)
        if uri and self.setting('REDIRECT_IS_HTTPS'):
            uri = uri.replace('http://', 'https://')
        return uri

    def get_language(self):
        """Return current language"""
        return ''

    def send_email_validation(self, email):
        email_validation = self.setting('EMAIL_VALIDATION_FUNCTION')
        send_email = module_member(email_validation)
        code = self.storage.code.make_code(email)
        send_email(self, code)
        return code

    def validate_email(self, email, code):
        verification_code = self.storage.code.get_code(code)
        if not verification_code or verification_code.code != code:
            return False
        else:
            verification_code.verify()
            return True

    def render_html(self, tpl=None, html=None, context=None):
        """Render given template or raw html with given context"""
        return self.tpl.render(tpl, html, context)

    # Implement the following methods on strategies sub-classes

    def redirect(self, url):
        """Return a response redirect to the given URL"""
        raise NotImplementedError('Implement in subclass')

    def get_setting(self, name):
        """Return value for given setting name"""
        raise NotImplementedError('Implement in subclass')

    def html(self, content):
        """Return HTTP response with given content"""
        raise NotImplementedError('Implement in subclass')

    def request_data(self, merge=True):
        """Return current request data (POST or GET)"""
        raise NotImplementedError('Implement in subclass')

    def request_host(self):
        """Return current host value"""
        raise NotImplementedError('Implement in subclass')

    def session_get(self, name, default=None):
        """Return session value for given key"""
        raise NotImplementedError('Implement in subclass')

    def session_set(self, name, value):
        """Set session value for given key"""
        raise NotImplementedError('Implement in subclass')

    def session_pop(self, name):
        """Pop session value for given key"""
        raise NotImplementedError('Implement in subclass')

    def build_absolute_uri(self, path=None):
        """Build absolute URI with given (optional) path"""
        raise NotImplementedError('Implement in subclass')
