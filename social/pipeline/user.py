from uuid import uuid4

from social.utils import slugify, module_member


USER_FIELDS = ['username', 'email']


def get_user(strategy, details, user=None, *args, **kwargs):
    if user:
        return {}

    if not user:
        username = kwargs['username']
        return {
            'user': strategy.storage.user.get_users_by_username(username).first()
        }


def get_username(strategy, details, user=None, *args, **kwargs):
    if 'username' not in strategy.setting('USER_FIELDS', USER_FIELDS):
        return
    storage = strategy.storage

    if not user:
        email_as_username = strategy.setting('USERNAME_IS_FULL_EMAIL', False)
        uuid_length = strategy.setting('UUID_LENGTH', 16)
        max_length = storage.user.username_max_length()
        do_slugify = strategy.setting('SLUGIFY_USERNAMES', False)
        do_clean = strategy.setting('CLEAN_USERNAMES', True)

        if do_clean:
            clean_func = storage.user.clean_username
        else:
            clean_func = lambda val: val

        if do_slugify:
            override_slug = strategy.setting('SLUGIFY_FUNCTION')
            if override_slug:
                slug_func = module_member(override_slug)
            else:
                slug_func = slugify
        else:
            slug_func = lambda val: val

        if email_as_username and details.get('email'):
            username = details['email']
        elif details.get('username'):
            username = details['username']
        else:
            username = uuid4().hex

        final_username = slug_func(clean_func(username[:max_length]))

    else:
        final_username = storage.user.get_username(user)

    return {'username': final_username}


def create_user(strategy, details, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name) or details.get(name))
                        for name in strategy.setting('USER_FIELDS',
                                                      USER_FIELDS))
    if not fields:
        return

    return {
        'is_new': True,
        'user': strategy.create_user(**fields)
    }


def user_details(strategy, details, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user:
        changed = False  # flag to track changes
        protected = ('username', 'id', 'pk') + \
                    tuple(strategy.setting('PROTECTED_USER_FIELDS', []))

        # Update user model attributes with the new data sent by the current
        # provider. Update on some attributes is disabled by default, for
        # example username and id fields. It's also possible to disable update
        # on fields defined in SOCIAL_AUTH_PROTECTED_FIELDS.
        for name, value in details.items():
            if not hasattr(user, name):
                continue
            current_value = getattr(user, name, None)
            if not current_value or name not in protected:
                changed |= current_value != value
                setattr(user, name, value)

        if changed:
            strategy.storage.user.changed(user)
