import time
import random
import hashlib

from social.utils import setting_name
from social.strategies.store import OpenIdStore


class BaseStrategy(object):
    ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyz' \
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                    '0123456789'

    def __init__(self, backend=None, storage=None, request=None,
                 *args, **kwargs):
        self.request = request
        self.storage = storage
        if backend:
            self.backend = backend(strategy=self, *args, **kwargs)
        else:
            self.backend = backend

    def setting(self, name, default=None):
        setting = default
        names = (setting_name(self.backend.titled_name, name),
                 setting_name(name),
                 name)
        for name in names:
            try:
                setting = self.get_setting(name)
            except AttributeError:
                pass
        return setting

    def get_setting(self, name):
        raise NotImplementedError('Implement in subclass')

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

    def disconnect(self, *args, **kwargs):
        self.storage.user.disconnect(name=self.backend.name, *args, **kwargs)

    def authenticate(self, *args, **kwargs):
        kwargs['strategy'] = self
        kwargs['storage'] = self.storage
        kwargs['backend'] = self.backend
        return self.backend.authenticate(*args, **kwargs)

    def redirect(self, url):
        return url

    def html(self, content):
        return content

    def create_user(self, *args, **kwargs):
        return self.storage.user.create_user(*args, **kwargs)

    def get_user(self, *args, **kwargs):
        return self.storage.user.get_user(*args, **kwargs)

    def request_data(self):
        raise NotImplementedError('Implement in subclass')

    def request_query_string(self):
        raise NotImplementedError('Implement in subclass')

    def request_host(self):
        raise NotImplementedError('Implement in subclass')

    def get_current_user(self, *args, **kwargs):
        raise NotImplementedError('Implement in subclass')

    def session_get(self, name):
        raise NotImplementedError('Implement in subclass')

    def session_set(self, name, value):
        raise NotImplementedError('Implement in subclass')

    def session_setdefault(self, name, value):
        self.session_set(name, value)
        return self.session_get(name)

    def to_session(self, next_idx, *args, **kwargs):
        raise NotImplementedError('Implement in subclass')

    def from_session(self, next_idx, *args, **kwargs):
        raise NotImplementedError('Implement in subclass')

    def build_absolute_uri(self, path=None):
        raise NotImplementedError('Implement in subclass')

    def clean_partial_pipeline(self):
        raise NotImplementedError('Implement in subclass')

    def openid_store(self):
        return OpenIdStore(self)

    def get_pipeline(self):
        return self.setting('PIPELINE', (
            'social.pipeline.social_auth.social_user',
            'social.pipeline.user.get_username',
            'social.pipeline.user.create_user',
            'social.pipeline.social_auth.associate_user',
            'social.pipeline.social_auth.load_extra_data',
            'social.pipeline.user.user_details'
       ))

    def random_string(self, length=12, chars=ALLOWED_CHARS):
        # Implementation borrowed from django 1.4
        try:
            random.SystemRandom()
        except NotImplementedError:
            random.seed(hashlib.sha256('%s%s%s' % (random.getstate(),
                                                   time.time(),
                                                   self.setting('SECRET_KEY')))
                               .digest())
        return ''.join([random.choice(chars) for i in range(length)])

    def is_integrity_error(self, exception):
        raise NotImplementedError('Implement in subclass')
