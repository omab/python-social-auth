def ask_for_password(strategy, *args, **kwargs):
    if strategy.session_get('password'):
        return {'password': strategy.session_get('password')}
    else:
        return strategy.redirect(strategy.build_absolute_uri('/password'))


def set_password(strategy, user, *args, **kwargs):
    user.set_password(kwargs['password'])
