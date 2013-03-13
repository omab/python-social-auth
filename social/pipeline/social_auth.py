from social.exceptions import AuthAlreadyAssociated


def social_user(strategy, uid, user=None, *args, **kwargs):
    provider = strategy.backend.name
    social_user = strategy.storage.user.get_social_auth(provider, uid)
    if social_user:
        if user and social_user.user != user:
            msg = 'This %s account is already in use.' % provider
            raise AuthAlreadyAssociated(strategy.backend, msg)
        elif not user:
            user = social_user.user
    return {'social_user': social_user,
            'user': user,
            'new_association': False}


def associate_user(strategy, user, uid, social_user=None, *args, **kwargs):
    if social_user or not user:
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
        return social_user(strategy.backend, uid, user,
                           social_user=social_user, *args, **kwargs)
    else:
        return {'social_user': social,
                'user': social.user,
                'new_association': True}


def load_extra_data(strategy, details, response, uid, user, social_user=None,
                    *args, **kwargs):
    social_user = social_user or \
                  strategy.storage.user.get_social_auth(strategy.backend.name,
                                                        uid)
    if social_user:
        extra_data = strategy.backend.extra_data(user, uid, response, details)
        social_user.set_extra_data(extra_data)
