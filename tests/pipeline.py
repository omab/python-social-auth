from social.pipeline.partial import partial


def ask_for_password(strategy, *args, **kwargs):
    if strategy.session_get('password'):
        return {'password': strategy.session_get('password')}
    else:
        return strategy.redirect(strategy.build_absolute_uri('/password'))


@partial
def ask_for_slug(strategy, *args, **kwargs):
    if strategy.session_get('slug'):
        return {'slug': strategy.session_get('slug')}
    else:
        return strategy.redirect(strategy.build_absolute_uri('/slug'))


def set_password(strategy, user, *args, **kwargs):
    user.set_password(kwargs['password'])


def set_slug(strategy, user, *args, **kwargs):
    user.slug = kwargs['slug']


def remove_user(strategy, user, *args, **kwargs):
    return {'user': None}
