from django.apps import AppConfig


class PythonSocialAuthConfig(AppConfig):
    name = 'social.apps.django_app.me'
    verbose_name = 'Python Social Auth'

    def ready(self):
        from social.strategies.utils import set_current_strategy_getter
        from social.apps.django_app.utils import load_strategy
        # Set strategy loader method to workaround current strategy getter
        # needed on get_user() method on authentication backends when working
        # with Django
        set_current_strategy_getter(load_strategy)
