"""Django ORM models for Social Auth"""
from django.db import models
from django.conf import settings

from social.storage.base import UserSocialAuthMixin, AssociationMixin, \
                                NonceMixin
from social.storage.django.fields import JSONField


USER_MODEL = getattr(settings, 'SOCIAL_AUTH_USER_MODEL', None) or \
             getattr(settings, 'AUTH_USER_MODEL', None) or \
             'auth.User'
UID_LENGTH = getattr(settings, 'SOCIAL_AUTH_UID_LENGTH', 255)


class UserSocialAuth(models.Model, UserSocialAuthMixin):
    """Social Auth association model"""
    user = models.ForeignKey(USER_MODEL, related_name='social_auth')
    provider = models.CharField(max_length=32)
    uid = models.CharField(max_length=UID_LENGTH)
    extra_data = JSONField(default='{}')

    class Meta:
        """Meta data"""
        unique_together = ('provider', 'uid')
        app_label = 'social_auth'

    @classmethod
    def get_social_auth(cls, provider, uid):
        try:
            return cls.objects.select_related('user').get(provider=provider,
                                                          uid=uid)
        except UserSocialAuth.DoesNotExist:
            return None

    @classmethod
    def user_model(cls):
        return UserSocialAuth._meta.get_field('user').rel.to


class Nonce(models.Model, NonceMixin):
    """One use numbers"""
    server_url = models.CharField(max_length=255)
    timestamp = models.IntegerField()
    salt = models.CharField(max_length=40)

    class Meta:
        app_label = 'social_auth'


class Association(models.Model, AssociationMixin):
    """OpenId account association"""
    server_url = models.CharField(max_length=255)
    handle = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)  # Stored base64 encoded
    issued = models.IntegerField()
    lifetime = models.IntegerField()
    assoc_type = models.CharField(max_length=64)

    class Meta:
        app_label = 'social_auth'
