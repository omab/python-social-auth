from django.apps import AppConfig


class PythonSocialAuthConfig(AppConfig):
    name = 'social.apps.django_app.default'
    verbose_name = 'Python Social Auth'

    def ready(self):
        from social.strategies.utils import set_current_strategy_getter
        from social.apps.django_app.utils import load_strategy
        set_current_strategy_getter(load_strategy)


