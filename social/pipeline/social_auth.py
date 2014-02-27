from social.exceptions import AuthAlreadyAssociated, AuthException, \
                              AuthForbidden


def social_details(strategy, response, *args, **kwargs):
    return {'details': strategy.backend.get_user_details(response)}


def social_uid(strategy, details, response, *args, **kwargs):
    return {'uid': strategy.backend.get_user_id(details, response)}


def auth_allowed(strategy, details, response, *args, **kwargs):
    if not strategy.backend.auth_allowed(response, details):
        raise AuthForbidden(strategy.backend)


def social_user(strategy, uid, user=None, *args, **kwargs):
    provider = strategy.backend.name
    social = strategy.storage.user.get_social_auth(provider, uid)
    if social:
        if user and social.user != user:
            msg = 'This {0} account is already in use.'.format(provider)
            raise AuthAlreadyAssociated(strategy.backend, msg)
        elif not user:
            user = social.user
    return {'social': social,
            'user': user,
            'is_new': user is None,
            'new_association': False}


def associate_user(strategy, uid, user=None, social=None, *args, **kwargs):
    if user and not social:
        try:
            social = strategy.storage.user.create_social_auth(
                user, uid, strategy.backend.name
            )
        except Exception as err:
            if not strategy.storage.is_integrity_error(err):
                raise
            # Protect for possible race condition, those bastard with FTL
            # clicking capabilities, check issue #131:
            #   https://github.com/omab/django-social-auth/issues/131
            return social_user(strategy, uid, user, *args, **kwargs)
        else:
            return {'social': social,
                    'user': social.user,
                    'new_association': True}


def associate_by_email(strategy, details, user=None, *args, **kwargs):
    """
    Associate current auth with a user with the same email address in the DB.

    This pipeline entry is not 100% secure unless you know that the providers
    enabled enforce email verification on their side, otherwise a user can
    attempt to take over another user account by using the same (not validated)
    email address on some provider.  This pipeline entry is disabled by
    default.
    """
    if user:
        return None

    email = details.get('email')
    if email:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        users = list(strategy.storage.user.get_users_by_email(email))
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise AuthException(
                strategy.backend,
                'The given email address is associated with another account'
            )
        else:
            return {'user': users[0]}


def load_extra_data(strategy, details, response, uid, user, *args, **kwargs):
    social = kwargs.get('social') or strategy.storage.user.get_social_auth(
        strategy.backend.name,
        uid
    )
    if social:
        extra_data = strategy.backend.extra_data(user, uid, response, details)
        social.set_extra_data(extra_data)
