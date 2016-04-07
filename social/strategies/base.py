import time
import random
import hashlib

from social.utils import setting_name, module_member
from social.store import OpenIdStore, OpenIdSessionWrapper
from social.pipeline import DEFAULT_AUTH_PIPELINE, DEFAULT_DISCONNECT_PIPELINE
from social.pipeline.utils import partial_from_session, partial_to_session


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
    DEFAULT_TEMPLATE_STRATEGY = BaseTemplateStrategy

    def __init__(self, storage=None, tpl=None):
        self.storage = storage
        self.tpl = (tpl or self.DEFAULT_TEMPLATE_STRATEGY)(self)

    def setting(self, name, default=None, backend=None):
        names = [setting_name(name), name]
        if backend:
            names.insert(0, setting_name(backend.name, name))
        for name in names:
            try:
                return self.get_setting(name)
            except (AttributeError, KeyError):
                pass
        return default

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
        return partial_to_session(self, next, backend, request=request,
                                  *args, **kwargs)

    def partial_from_session(self, session):
        return partial_from_session(self, session)

    def clean_partial_pipeline(self, name='partial_pipeline'):
        self.session_pop(name)

    def openid_store(self):
        return OpenIdStore(self)

    def get_pipeline(self):
        return self.setting('SOCIAL_AUTH_PIPELINE', DEFAULT_AUTH_PIPELINE)

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

    def send_email_validation(self, backend, email):
        email_validation = self.setting('EMAIL_VALIDATION_FUNCTION')
        send_email = module_member(email_validation)
        code = self.storage.code.make_code(email)
        send_email(self, backend, code)
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

    def authenticate(self, backend, *args, **kwargs):
        """Trigger the authentication mechanism tied to the current
        framework"""
        kwargs['strategy'] = self
        kwargs['storage'] = self.storage
        kwargs['backend'] = backend
        return backend.authenticate(*args, **kwargs)

    def get_backends(self):
        """Return configured backends"""
        return self.setting('AUTHENTICATION_BACKENDS', [])

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

    def request_is_secure(self):
        """Is the request using HTTPS?"""
        raise NotImplementedError('Implement in subclass')

    def request_path(self):
        """path of the current request"""
        raise NotImplementedError('Implement in subclass')

    def request_port(self):
        """Port in use for this request"""
        raise NotImplementedError('Implement in subclass')

    def request_get(self):
        """Request GET data"""
        raise NotImplementedError('Implement in subclass')

    def request_post(self):
        """Request POST data"""
        raise NotImplementedError('Implement in subclass')
