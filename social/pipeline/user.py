from uuid import uuid4


def get_username(strategy, details, user=None, *args, **kwargs):
    storage = strategy.storage

    if not user:
        username = unicode(details.get('username') or uuid4().get_hex())
        uuid_length = strategy.setting('UUID_LENGTH', 16)
        max_length = storage.user.username_max_length()
        short_username = username[:max_length - uuid_length]
        final_username = storage.user.clean_username(username[:max_length])

        # Generate a unique username for current user using username
        # as base but adding a unique hash at the end. Original
        # username is cut to avoid any field max_length.
        while storage.user.simple_user_exists(username=final_username):
            username = short_username + uuid4().get_hex()[:uuid_length]
            final_username = storage.user.clean_username(username[:max_length])
    else:
        final_username = storage.user.get_username(user)
    return {'username': final_username}


def create_user(strategy, details, response, uid, username, user=None, *args,
                **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user or not username:
        return None
    return {
        'is_new': True,
        'user': strategy.storage.user.create_user(username=username,
                                                  email=details.get('email'))
    }


def user_details(strategy, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    if user is None:
        return

    changed = False  # flag to track changes
    if kwargs.get('is_new'):
        keep = ('username', 'id', 'pk')
    else:
        keep = strategy.setting('PROTECTED_USER_FIELDS', [])

    for name, value in details.iteritems():
        # do not update username, it was already generated
        # do not update configured fields if user already existed
        if name not in keep:
            if value and value != getattr(user, name, None):
                setattr(user, name, value)
                changed = True
    if changed:
        strategy.storage.user.changed(user)
