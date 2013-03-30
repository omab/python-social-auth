from social.p3 import quote
from social.utils import sanitize_redirect, user_is_authenticated, \
                         user_is_active


def do_auth(strategy, redirect_name='next'):
    # Save any defined next value into session
    data = strategy.request_data(merge=False)

    # Save extra data into session.
    for field_name in strategy.setting('FIELDS_STORED_IN_SESSION', []):
        if field_name in data:
            strategy.session_set(field_name, data[field_name])

    if redirect_name in data:
        # Check and sanitize a user-defined GET/POST next field value
        redirect_uri = data[redirect_name]
        if strategy.setting('SANITIZE_REDIRECTS', True):
            redirect_uri = sanitize_redirect(strategy.request_host(),
                                             redirect_uri)
        strategy.session_set(
            redirect_name,
            redirect_uri or strategy.setting('LOGIN_REDIRECT_URL')
        )
    return strategy.start()


def do_complete(strategy, login, user=None, redirect_name='next',
                *args, **kwargs):
    # pop redirect value before the session is trashed on login()
    data = strategy.request_data()
    redirect_value = strategy.session_get(redirect_name, '') or \
                     data.get(redirect_name, '')

    is_authenticated = user_is_authenticated(user)
    user = is_authenticated and user or None
    default_redirect = strategy.setting('LOGIN_REDIRECT_URL')
    url = default_redirect
    login_error_url = strategy.setting('LOGIN_ERROR_URL') or \
                      strategy.setting('LOGIN_URL')

    if strategy.session_get('partial_pipeline'):
        idx, backend, xargs, xkwargs = strategy.from_session(
            strategy.session_pop('partial_pipeline')
        )
        if backend == strategy.backend_name:
            kwargs = kwargs.copy()
            kwargs.setdefault('user', user)
            kwargs.update(xkwargs)
            user = strategy.continue_pipeline(pipeline_index=idx,
                                              *xargs, **xkwargs)
        else:
            strategy.clean_partial_pipeline()
            user = strategy.complete(user=user, request=strategy.request,
                                     *args, **kwargs)
    else:
        user = strategy.complete(user=user, request=strategy.request,
                                 *args, **kwargs)

    if strategy.is_response(user):
        return user

    if is_authenticated:
        if not user:
            url = redirect_value or default_redirect
        else:
            url = redirect_value or \
                  strategy.setting('NEW_ASSOCIATION_REDIRECT_URL') or \
                  default_redirect
    elif user:
        if user_is_active(user):
            # catch is_new/social_user in case login() resets the instance
            is_new = getattr(user, 'is_new', False)
            social_user = user.social_user
            login(strategy, user)
            # store last login backend name in session
            strategy.session_set('social_auth_last_login_backend',
                                 social_user.provider)

            # Remove possible redirect URL from session, if this is a new
            # account, send him to the new-users-page if defined.
            new_user_redirect = strategy.setting('NEW_USER_REDIRECT_URL')
            if new_user_redirect and is_new:
                url = new_user_redirect
            else:
                url = redirect_value or default_redirect
        else:
            url = strategy.setting('INACTIVE_USER_URL', login_error_url)
    else:
        url = login_error_url

    if redirect_value and redirect_value != url:
        redirect_value = quote(redirect_value)
        url += ('?' in url and '&' or '?') + \
               '%s=%s' % (redirect_name, redirect_value)
    return strategy.redirect(url)


def do_disconnect(strategy, user, association_id=None, redirect_name='next'):
    strategy.disconnect(user=user, association_id=association_id)
    data = strategy.request_data()
    return strategy.redirect(data.get(redirect_name, '') or
                             strategy.setting('DISCONNECT_REDIRECT_URL') or
                             strategy.setting('LOGIN_REDIRECT_URL'))
