"""Models mixins for Social Auth"""
import base64
import time
from datetime import datetime, timedelta

from openid.association import Association as OIDAssociation

from social.utils import utc


# django.contrib.auth and mongoengine.django.auth regex to validate usernames
# '^[\w@.+-_]+$', we use the opposite to clean invalid characters

class UserSocialAuthMixin(object):
    user = ''
    provider = ''

    def __unicode__(self):
        """Return associated user unicode representation"""
        return u'%s - %s' % (unicode(self.user), self.provider.title())

    def get_backend(self):
        # Make import here to avoid recursive imports :-/
        from social_auth.backends import get_backends
        return get_backends().get(self.provider)

    @property
    def tokens(self):
        """Return access_token stored in extra_data or None"""
        backend = self.get_backend()
        if backend:
            return backend.AUTH_BACKEND.tokens(self)
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
                    backend.AUTH_BACKEND.extra_data(self.user, self.uid,
                                                    response)
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

    @classmethod
    def user_model(cls):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def username_max_length(cls):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def clean_username(cls, value):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def simple_user_exists(cls, *args, **kwargs):
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

    @classmethod
    def store_association(cls, server_url, association):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_oid_associations(cls, server_url, handle=None):
        kwargs = {'server_url': server_url}
        if handle is not None:
            kwargs['handle'] = handle
        return sorted([
                (assoc.id,
                 OIDAssociation(assoc.handle,
                                base64.decodestring(assoc.secret),
                                assoc.issued,
                                assoc.lifetime,
                                assoc.assoc_type))
                for assoc in cls.get_associations(**kwargs)
        ], key=lambda x: x[1].issued, reverse=True)

    @classmethod
    def get_associations(cls, *args, **kwargs):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def delete_associations(cls, ids_to_delete):
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def use_nonce(cls, server_url, timestamp, salt):
        raise NotImplementedError('Implement in subclass')


class NonceMixin(object):
    """One use numbers"""
    server_url = ''
    timestamp = 0
    salt = ''

    def __unicode__(self):
        """Unicode representation"""
        return self.server_url


class AssociationMixin(object):
    """OpenId account association"""
    server_url = ''
    handle = ''
    secret = ''
    issued = 0
    lifetime = 0
    assoc_type = ''

    def __unicode__(self):
        """Unicode representation"""
        return '%s %s' % (self.handle, self.issued)
