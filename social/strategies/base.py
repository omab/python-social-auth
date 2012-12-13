import time
import random
import hashlib


SETTING_PREFIX = 'SOCIAL_AUTH'

try:
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False


class BaseStrategy(object):
    ALLOWED_CHARS = 'abcdefghijklmnopqrstuvwxyz' \
                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                    '0123456789'

    def __init__(self, backend, storage, request):
        self.backend = backend
        self.storage = storage
        self.request = request

    def setting(self, name, default=None):
        setting_name = '_'.join((SETTING_PREFIX, self.backend.titled_name,
                                 name))
        setting = self.get_setting(setting_name, default)
        if not setting:
            setting = self.get_setting('%s_%s' % (SETTING_PREFIX, name),
                                       default)
        return setting

    def get_setting(self, name, default=None):
        raise NotImplementedError('Implement in subclass')

    def request_data(self):
        if not hasattr(self, '_request'):
            self._request = {}
        return self._request

    def request_query_string(self):
        return self.request.META.get('QUERY_STRING', '')

    def start(self):
        if self.backend.uses_redirect():
            return self.redirect(self.backend.auth_url())
        else:
            return self.html(self.backend.auth_html())

    def complete_login(self, *args, **kwargs):
        return self.backend.auth_complete(*args, **kwargs)

    def complete_associate(self, user, *args, **kwargs):
        return self.backend.auth_complete(user=user, *args, **kwargs)

    def continue_pipeline(self):
        raise NotImplementedError('Implement in subclass')

    def disconnect(self, *args, **kwargs):
        self.storage.disconnect(name=self.backend.name, *args, **kwargs)

    def authenticate(self, *args, **kwargs):
        return self.backend.authenticate(*args, **kwargs)

    def redirect(self, url):
        return url

    def html(self, content):
        return content

    def create_user(self, *args, **kwargs):
        return self.storage.create_user(*args, **kwargs)

    def get_user(self, *args, **kwargs):
        return self.storage.get_user(*args, **kwargs)

    def get_current_user(self, *args, **kwargs):
        raise NotImplementedError('Implement in subclass')

    def session_get(self, name):
        raise NotImplementedError('Implement in subclass')

    def session_set(self, name, value):
        raise NotImplementedError('Implement in subclass')

    def session_setdefault(self, name, value):
        self.session_set(name, value)

    def to_session_dict(self, next_idx, *args, **kwargs):
        raise NotImplementedError('Implement in subclass')

    def from_session_dict(self, next_idx, *args, **kwargs):
        raise NotImplementedError('Implement in subclass')

    def build_absolute_uri(self, path=None):
        raise NotImplementedError('Implement in subclass')

    def clean_partial_pipeline(self):
        raise NotImplementedError('Implement in subclass')

    def openid_store(self):
        raise NotImplementedError('Implement in subclass')

    def get_pipeline(self):
        return self.setting('PIPELINE', (
            'social.pipeline.social.social_auth_user',
            'social.pipeline.user.get_username',
            'social.pipeline.user.create_user',
            'social.pipeline.social.associate_user',
            'social.pipeline.social.load_extra_data',
            'social.pipeline.user.update_user_details'
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
