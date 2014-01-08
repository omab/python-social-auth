"""Django ORM models for Social Auth"""
import six

from django.db import models
from django.conf import settings
from django.db.utils import IntegrityError

from social.utils import setting_name
from social.storage.django_orm import DjangoUserMixin, \
                                      DjangoAssociationMixin, \
                                      DjangoNonceMixin, \
                                      DjangoCodeMixin, \
                                      BaseDjangoStorage
from social.apps.django_app.default.fields import JSONField


USER_MODEL = getattr(settings, setting_name('USER_MODEL'), None) or \
             getattr(settings, 'AUTH_USER_MODEL', None) or \
             'auth.User'
UID_LENGTH = getattr(settings, setting_name('UID_LENGTH'), 255)
NONCE_SERVER_URL_LENGTH = getattr(
    settings, setting_name('NONCE_SERVER_URL_LENGTH'), 255)
ASSOCIATION_SERVER_URL_LENGTH = getattr(
    settings, setting_name('ASSOCIATION_SERVER_URL_LENGTH'), 255)
ASSOCIATION_HANDLE_LENGTH = getattr(
    settings, setting_name('ASSOCIATION_HANDLE_LENGTH'), 255)


class UserSocialAuth(models.Model, DjangoUserMixin):
    """Social Auth association model"""
    user = models.ForeignKey(USER_MODEL, related_name='social_auth')
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=UID_LENGTH)
    extra_data = JSONField()

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')
        db_table = 'social_auth_usersocialauth'

    @classmethod
    def get_social_auth(cls, provider, uid):
        try:
            return cls.objects.select_related('user').get(provider=provider,
                                                          uid=uid)
        except UserSocialAuth.DoesNotExist:
            return None

    @classmethod
    def username_max_length(cls):
        username_field = cls.username_field()
        field = UserSocialAuth.user_model()._meta.get_field(username_field)
        return field.max_length

    @classmethod
    def user_model(cls):
        user_model = UserSocialAuth._meta.get_field('user').rel.to
        if isinstance(user_model, six.string_types):
            app_label, model_name = user_model.split('.')
            return models.get_model(app_label, model_name)
        return user_model


class Nonce(models.Model, DjangoNonceMixin):
    """One use numbers"""
    server_url = models.CharField(max_length=NONCE_SERVER_URL_LENGTH)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=65)

    class Meta:
        db_table = 'social_auth_nonce'


class Association(models.Model, DjangoAssociationMixin):
    """OpenId account association"""
    server_url = models.CharField(max_length=ASSOCIATION_SERVER_URL_LENGTH)
    handle = models.CharField(max_length=ASSOCIATION_HANDLE_LENGTH)
    secret = models.CharField(max_length=255)  # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        db_table = 'social_auth_association'


class Code(models.Model, DjangoCodeMixin):
    email = models.EmailField()
    code = models.CharField(max_length=32, db_index=True)
    verified = models.BooleanField(default=False)

    class Meta:
        db_table = 'social_auth_code'
        unique_together = ('email', 'code')


class DjangoStorage(BaseDjangoStorage):
    user = UserSocialAuth
    nonce = Nonce
    association = Association
    code = Code

    @classmethod
    def is_integrity_error(cls, exception):
        return exception.__class__ is IntegrityError
