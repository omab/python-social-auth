"""
MongoEngine models for Social Auth

Requires MongoEngine 0.6.10
"""
import six

from django.conf import settings

from mongoengine import DictField, Document, IntField, ReferenceField, \
                        StringField, EmailField, BooleanField
from mongoengine.queryset import OperationError

from social.utils import setting_name, module_member
from social.storage.django_orm import DjangoUserMixin, \
                                      DjangoAssociationMixin, \
                                      DjangoNonceMixin, \
                                      DjangoCodeMixin, \
                                      BaseDjangoStorage


UNUSABLE_PASSWORD = '!'  # Borrowed from django 1.4


def _get_user_model():
    """
    Get the User Document class user for MongoEngine authentication.

    Use the model defined in SOCIAL_AUTH_USER_MODEL if defined, or
    defaults to MongoEngine's configured user document class.
    """
    custom_model = getattr(settings, setting_name('USER_MODEL'), None)
    if custom_model:
        return module_member(custom_model)

    try:
        # Custom user model support with MongoEngine 0.8
        from mongoengine.django.mongo_auth.models import get_user_document
        return get_user_document()
    except ImportError:
        return module_member('mongoengine.django.auth.User')


USER_MODEL = _get_user_model()


class UserSocialAuth(Document, DjangoUserMixin):
    """Social Auth association model"""
    user = ReferenceField(USER_MODEL)
    provider = StringField(max_length=32)
    uid = StringField(max_length=255, unique_with='provider')
    extra_data = DictField()

    def str_id(self):
        return str(self.id)

    @classmethod
    def get_social_auth_for_user(cls, user, provider=None, id=None):
        qs = cls.objects
        if provider:
            qs = qs.filter(provider=provider)
        if id:
            qs = qs.filter(id=id)
        return qs.filter(user=user)

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        if not isinstance(type(uid), six.string_types):
            uid = str(uid)
        return cls.objects.create(user=user, uid=uid, provider=provider)

    @classmethod
    def username_max_length(cls):
        username_field = cls.username_field()
        field = getattr(UserSocialAuth.user_model(), username_field)
        return field.max_length

    @classmethod
    def user_model(cls):
        return USER_MODEL

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


class Code(Document, DjangoCodeMixin):
    email = EmailField()
    code = StringField(max_length=32)
    verified = BooleanField(default=False)


class DjangoStorage(BaseDjangoStorage):
    user = UserSocialAuth
    nonce = Nonce
    association = Association
    code = Code

    @classmethod
    def is_integrity_error(cls, exception):
        return exception.__class__ is OperationError and \
               'E11000' in exception.message
