"""
MongoEngine models for Social Auth

Requires MongoEngine 0.6.10
"""
from mongoengine import DictField, Document, IntField, ReferenceField, \
                        StringField
from mongoengine.django.auth import User
from mongoengine.queryset import OperationError

from social.storage.django_orm import DjangoUserMixin, \
                                      DjangoAssociationMixin, \
                                      DjangoNonceMixin, \
                                      BaseDjangoStorage


UNUSABLE_PASSWORD = '!'  # Borrowed from django 1.4


class UserSocialAuth(Document, DjangoUserMixin):
    """Social Auth association model"""
    user = ReferenceField(User)
    provider = StringField(max_length=32)
    uid = StringField(max_length=255, unique_with='provider')
    extra_data = DictField()

    @classmethod
    def get_social_auth_for_user(cls, user):
        return cls.objects(user=user)

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        if not isinstance(type(uid), basestring):
            uid = str(uid)
        return cls.objects.create(user=user, uid=uid, provider=provider)

    @classmethod
    def username_max_length(cls):
        return UserSocialAuth.user_model().username.max_length

    @classmethod
    def user_model(cls):
        return User

    @classmethod
    def create_user(cls, username, email=None):
        # Empty string makes email regex validation fail
        email = email or None
        return cls.user_model().create_user(username=username,
                                            password=UNUSABLE_PASSWORD,
                                            email=email)

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

    def is_integrity_error(self, exception):
        return exception.__class__ is OperationError and \
               'E11000' in exception.message
