"""Django ORM models for Social Auth"""
import re
import base64

from social.exceptions import NotAllowedToDisconnect
from social.storage.base import UserSocialAuthMixin


CLEAN_USERNAME_REGEX = re.compile(r'[^\w.@+-_]+', re.UNICODE)


class DjangoUserSocialAuthMixin(UserSocialAuthMixin):
    """Social Auth association model"""
    @classmethod
    def clean_username(cls, value):
        return CLEAN_USERNAME_REGEX.sub('', value)

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        if association_id is not None:
            qs = cls.objects.exclude(id=association_id)
        else:
            qs = cls.objects.exclude(provider=backend_name)

        if hasattr(user, 'has_usable_password'):
            valid_password = user.has_usable_password()
        else:
            valid_password = True
        return valid_password or qs.count() > 0

    @classmethod
    def disconnect(cls, name, user, association_id=None):
        if cls.allowed_to_disconnect(user, name, association_id):
            qs = cls.get_social_auth_for_user(user)
            if association_id:
                qs = qs.get(id=association_id)
            else:
                qs = qs.filter(provider=name)
            qs.delete()
        else:
            raise NotAllowedToDisconnect()

    @classmethod
    def simple_user_exists(cls, *args, **kwargs):
        """
        Return True/False if a User instance exists with the given arguments.
        Arguments are directly passed to filter() manager method.
        """
        return cls.user_model().objects.filter(*args, **kwargs).count() > 0

    @classmethod
    def create_user(cls, username, email=None):
        return cls.user_model().objects.create_user(username=username,
                                                    email=email)

    @classmethod
    def get_user(cls, pk):
        try:
            return cls.user_model().objects.get(pk=pk)
        except cls.user_model().DoesNotExist:
            return None

    @classmethod
    def get_social_auth(cls, provider, uid):
        if not isinstance(uid, basestring):
            uid = str(uid)
        try:
            return cls.objects.get(provider=provider, uid=uid)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_social_auth_for_user(cls, user):
        return user.social_auth.all()

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        if not isinstance(uid, basestring):
            uid = str(uid)
        return cls.objects.create(user=user, uid=uid, provider=provider)

    @classmethod
    def store_association(cls, server_url, association):
        from social.models import Association
        args = {'server_url': server_url, 'handle': association.handle}
        try:
            assoc = Association.objects.get(**args)
        except Association.DoesNotExist:
            assoc = Association(**args)
        assoc.secret = base64.encodestring(association.secret)
        assoc.issued = association.issued
        assoc.lifetime = association.lifetime
        assoc.assoc_type = association.assoc_type
        assoc.save()

    @classmethod
    def get_associations(cls, *args, **kwargs):
        from social.models import Association
        return Association.objects.filter(*args, **kwargs)

    @classmethod
    def delete_associations(cls, ids_to_delete):
        from social.models import Association
        Association.objects.filter(pk__in=ids_to_delete).delete()

    @classmethod
    def use_nonce(cls, server_url, timestamp, salt):
        from social.models import Nonce
        return Nonce.objects.get_or_create(server_url=server_url,
                                           timestamp=timestamp,
                                           salt=salt)[1]
