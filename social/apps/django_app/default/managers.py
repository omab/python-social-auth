from django.db import models


class UserSocialAuthManager(models.Manager):
    """Manager for the UserSocialAuth django model."""

    def get_social_auth(self, provider, uid, provider_domain=None):
        try:
            return self.select_related('user').get(
                provider=provider, uid=uid,
                provider_domain=provider_domain)
        except self.model.DoesNotExist:
            return None
