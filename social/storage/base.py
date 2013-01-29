"""Models mixins for Social Auth"""
import re
import time
import base64
from datetime import datetime, timedelta

from openid.association import Association as OpenIdAssociation

from social.utils import utc


CLEAN_USERNAME_REGEX = re.compile(r'[^\w.@+-_]+', re.UNICODE)


class UserMixin(object):
    user = ''
    provider = ''
    uid = None
    extra_data = None

    def get_backend(self):
        # Make import here to avoid recursive imports :-/
        from social_auth.backends import get_backends
        return get_backends().get(self.provider)

    @property
    def tokens(self):
        """Return access_token stored in extra_data or None"""
        backend = self.get_backend()
        if backend:
            return backend.tokens(self)
        else:
            return {}

    def refresh_token(self):
        data = self.extra_data
        if 'refresh_token' in data or 'access_token' in data:
            backend = self.get_backend()
            if hasattr(backend, 'refresh_token'):
                token = data.get('refresh_token') or data.get('access_token')
                response = backend.refresh_token(token)
                self.extra_data.update(
                    backend.extra_data(self.user, self.uid, response)
                )
                self.save()

    def expiration_datetime(self):
        """Return provider session live seconds. Returns a timedelta ready to
        use with session.set_expiry().

        If provider returns a timestamp instead of session seconds to live, the
        timedelta is inferred from current time (using UTC timezone). None is
        returned if there's no value stored or it's invalid.
        """
        if self.extra_data and 'expires' in self.extra_data:
            try:
                expires = int(self.extra_data.get('expires'))
            except (ValueError, TypeError):
                return None

            now = datetime.now()
            now_timestamp = time.mktime(now.timetuple())

            # Detect if expires is a timestamp
            if expires > now_timestamp:  # expires is a datetime
                return datetime.utcfromtimestamp(expires) \
                               .replace(tzinfo=utc) - \
                       now.replace(tzinfo=utc)
            else:  # expires is a timedelta
                return timedelta(seconds=expires)

    def set_extra_data(self, extra_data=None):
        if extra_data and self.extra_data != extra_data:
            if self.extra_data:
                self.extra_data.update(extra_data)
            else:
                self.extra_data = extra_data
            return True

    @classmethod
    def changed(cls, user):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_username(cls, user):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def user_model(cls):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def username_max_length(cls):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def clean_username(cls, value):
        return CLEAN_USERNAME_REGEX.sub('', value)

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def disconnect(cls, name, user, association_id=None):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def simple_user_exists(cls, username):
        """
        Return True/False if a User instance exists with the given arguments.
        Arguments are directly passed to filter() manager method.
        """
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def create_user(cls, username, email=None):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_user(cls, pk):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_social_auth(cls, provider, uid):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_social_auth_for_user(cls, user):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        raise NotImplementedError('Implement in subclass')


class NonceMixin(object):
    """One use numbers"""
    server_url = ''
    timestamp = 0
    salt = ''

    @classmethod
    def use(cls, server_url, timestamp, salt):
        raise NotImplementedError('Implement in subclass')


class AssociationMixin(object):
    """OpenId account association"""
    server_url = ''
    handle = ''
    secret = ''
    issued = 0
    lifetime = 0
    assoc_type = ''

    @classmethod
    def store(cls, server_url, association):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get(cls, *args, **kwargs):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def remove(cls, ids_to_delete):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def oids(cls, server_url, handle=None):
        kwargs = {'server_url': server_url}
        if handle is not None:
            kwargs['handle'] = handle
        return sorted([
                (assoc.id,
                 OpenIdAssociation(assoc.handle,
                                   base64.decodestring(assoc.secret),
                                   assoc.issued,
                                   assoc.lifetime,
                                   assoc.assoc_type))
                for assoc in cls.get(**kwargs)
        ], key=lambda x: x[1].issued, reverse=True)


class BaseStorage(object):
    user = UserMixin
    nonce = NonceMixin
    association = AssociationMixin

    @classmethod
    def is_integrity_error(cls, exception):
        raise NotImplementedError('Implement in subclass')
