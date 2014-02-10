"""Admin settings"""
from django.contrib import admin
from social.apps.django_app.default.models import UserSocialAuth, Nonce, \
                                                  Association


_User = UserSocialAuth.user_model()

username = getattr(_User, 'USERNAME_FIELD', None) or \
           hasattr(_User, 'username') and 'username' or \
           None
fieldnames = ('first_name', 'last_name', 'email', username)
all_names = _User._meta.get_all_field_names()
user_search_fields = ['user__' + name for name in fieldnames
                            if name and name in all_names]


class UserSocialAuthOption(admin.ModelAdmin):
    """Social Auth user options"""
    list_display = ('id', 'user', 'provider', 'uid')
    search_fields = user_search_fields
    list_filter = ('provider',)
    raw_id_fields = ('user',)
    list_select_related = True


class NonceOption(admin.ModelAdmin):
    """Nonce options"""
    list_display = ('id', 'server_url', 'timestamp', 'salt')
    search_fields = ('server_url',)


class AssociationOption(admin.ModelAdmin):
    """Association options"""
    list_display = ('id', 'server_url', 'assoc_type')
    list_filter = ('assoc_type',)
    search_fields = ('server_url',)


admin.site.register(UserSocialAuth, UserSocialAuthOption)
admin.site.register(Nonce, NonceOption)
admin.site.register(Association, AssociationOption)
