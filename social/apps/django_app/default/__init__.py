"""
Django default ORM backend support.

To enable this app:
    * Add 'social.apps.django_app.default' to INSTALLED_APPS
    * In urls.py include url('', include('social.apps.django_app.urls'))
"""

default_app_config = \
    'social.apps.django_app.default.config.PythonSocialAuthConfig'
