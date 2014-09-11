from django.conf import settings
from django.db.models.loading import get_model


def get_custom_user_model_for_migrations():
    user_model = getattr(settings, 'SOCIAL_AUTH_USER_MODEL', None) or \
                 getattr(settings, 'AUTH_USER_MODEL', None) or \
                 'auth.User'
    if user_model != 'auth.User':
        # In case of having a proxy model defined as USER_MODEL
        # We use auth.User instead to prevent migration errors
        # Since proxy models aren't present in migrations
        if get_model(*user_model.split('.'))._meta.proxy:
            user_model = 'auth.User'
    return user_model


def custom_user_frozen_models(user_model):
    migration_name = getattr(settings, 'INITIAL_CUSTOM_USER_MIGRATION',
                             '0001_initial.py')
    if user_model != 'auth.User':
        from south.migration.base import Migrations
        from south.exceptions import NoMigrations
        from south.creator.freezer import freeze_apps
        user_app, user_model = user_model.split('.')
        try:
            user_migrations = Migrations(user_app)
        except NoMigrations:
            extra_model = freeze_apps(user_app)
        else:
            initial_user_migration = user_migrations.migration(migration_name)
            extra_model = initial_user_migration.migration_class().models
    else:
        extra_model = {}
    return extra_model
