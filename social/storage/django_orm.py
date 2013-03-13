"""Django ORM models for Social Auth"""
import base64
import six

from social.exceptions import NotAllowedToDisconnect
from social.storage.base import UserMixin, AssociationMixin, NonceMixin, \
                                BaseStorage


class DjangoUserMixin(UserMixin):
    """Social Auth association model"""
    @classmethod
    def changed(cls, user):
        user.save()

    def set_extra_data(self, extra_data=None):
        if super(DjangoUserMixin, self).set_extra_data(extra_data):
            self.save()

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        if association_id is not None:
            qs = cls.objects.exclude(id=association_id)
        else:
            qs = cls.objects.exclude(provider=backend_name)
        qs = qs.filter(user=user)

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
    def user_exists(cls, username):
        """
        Return True/False if a User instance exists with the given arguments.
        Arguments are directly passed to filter() manager method.
        """
        return cls.user_model().objects.filter(username=username).count() > 0

    @classmethod
    def get_username(cls, user):
        return getattr(user, 'username', None)

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
        if not isinstance(uid, six.string_types):
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
        if not isinstance(uid, six.string_types):
            uid = str(uid)
        return cls.objects.create(user=user, uid=uid, provider=provider)


class DjangoNonceMixin(NonceMixin):
    @classmethod
    def use(cls, server_url, timestamp, salt):
        return cls.objects.get_or_create(server_url=server_url,
                                         timestamp=timestamp,
                                         salt=salt)[1]


class DjangoAssociationMixin(AssociationMixin):
    @classmethod
    def store(cls, server_url, association):
        # Don't use get_or_create because issued cannot be null
        try:
            assoc = cls.objects.get(server_url=server_url,
                                    handle=association.handle)
        except cls.DoesNotExist:
            assoc = cls(server_url=server_url,
                        handle=association.handle)
        assoc.secret = base64.encodestring(association.secret)
        assoc.issued = association.issued
        assoc.lifetime = association.lifetime
        assoc.assoc_type = association.assoc_type
        assoc.save()

    @classmethod
    def get(cls, *args, **kwargs):
        return cls.objects.filter(*args, **kwargs)

    @classmethod
    def remove(cls, ids_to_delete):
        cls.objects.filter(pk__in=ids_to_delete).delete()


class BaseDjangoStorage(BaseStorage):
    user = DjangoUserMixin
    nonce = DjangoNonceMixin
    association = DjangoAssociationMixin
