"""
MongoEngine models for Social Auth

Requires MongoEngine 0.6.10
"""
import six

from django.conf import settings

from mongoengine import DictField, Document, IntField, ReferenceField, \
                        StringField
from mongoengine.django.auth import User
from mongoengine.queryset import OperationError

from social.utils import setting_name, module_member
from social.storage.django_orm import DjangoUserMixin, \
                                      DjangoAssociationMixin, \
                                      DjangoNonceMixin, \
                                      BaseDjangoStorage


UNUSABLE_PASSWORD = '!'  # Borrowed from django 1.4


USER_MODEL = module_member(
    getattr(settings, setting_name('USER_MODEL'), None) or
    getattr(settings, 'AUTH_USER_MODEL', None) or
    'mongoengine.django.auth.User'
)


class UserSocialAuth(Document, DjangoUserMixin):
    """Social Auth association model"""
    user = ReferenceField(USER_MODEL, dbref=True)
    provider = StringField(max_length=32)
    uid = StringField(max_length=255, unique_with='provider')
    extra_data = DictField()

    @classmethod
    def get_social_auth_for_user(cls, user):
        return cls.objects(user=user)

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        if not isinstance(type(uid), six.string_types):
            uid = str(uid)
        return cls.objects.create(user=user, uid=uid, provider=provider)

    @classmethod
    def username_max_length(cls):
        return UserSocialAuth.user_model().username.max_length

    @classmethod
    def user_model(cls):
        return User

    @classmethod
    def create_user(cls, *args, **kwargs):
        kwargs['password'] = UNUSABLE_PASSWORD
        if 'email' in kwargs:
            # Empty string makes email regex validation fail
            kwargs['email'] = kwargs['email'] or None
        return cls.user_model().create_user(*args, **kwargs)

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        if association_id is not None:
            qs = cls.objects.filter(id__ne=association_id)
        else:
            qs = cls.objects.filter(provider__ne=backend_name)
        qs = qs.filter(user=user)

        if hasattr(user, 'has_usable_password'):
            valid_password = user.has_usable_password()
        else:
            valid_password = True

        return valid_password or qs.count() > 0


class Nonce(Document, DjangoNonceMixin):
    """One use numbers"""
    server_url = StringField(max_length=255)
    timestamp = IntField()
    salt = StringField(max_length=40)


class Association(Document, DjangoAssociationMixin):
    """OpenId account association"""
    server_url = StringField(max_length=255)
    handle = StringField(max_length=255)
    secret = StringField(max_length=255)  # Stored base64 encoded
    issued = IntField()
    lifetime = IntField()
    assoc_type = StringField(max_length=64)


class DjangoStorage(BaseDjangoStorage):
    user = UserSocialAuth
    nonce = Nonce
    association = Association

    @classmethod
    def is_integrity_error(cls, exception):
        return exception.__class__ is OperationError and \
               'E11000' in exception.message
