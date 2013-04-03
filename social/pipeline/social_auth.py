from social.exceptions import AuthAlreadyAssociated


def social_user(strategy, uid, user=None, *args, **kwargs):
    provider = strategy.backend.name
    social = strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            msg = 'This %s account is already in use.' % provider
            raise AuthAlreadyAssociated(strategy.backend, msg)
        elif not user:
            user = social.user
    return {'social': social,
            'user': user,
            'new_association': False}


def associate_user(strategy, user, uid, *args, **kwargs):
    if kwargs.get('social') or not user:
        return None

    try:
        social = strategy.storage.user.create_social_auth(
            user, uid, strategy.backend.name
        )
    except Exception as err:
        if not strategy.is_integrity_error(err):
            raise
        # Protect for possible race condition, those bastard with FTL
        # clicking capabilities, check issue #131:
        #   https://github.com/omab/django-social-auth/issues/131
        return social_user(strategy, uid, user, *args, **kwargs)
    else:
        return {'social': social,
                'user': social.user,
                'new_association': True}


def load_extra_data(strategy, details, response, uid, user, *args, **kwargs):
    social = kwargs.get('social') or \
             strategy.storage.user.get_social_auth(strategy.backend.name,
                                                        uid)
    if social:
        extra_data = strategy.backend.extra_data(user, uid, response, details)
        social.set_extra_data(extra_data)
