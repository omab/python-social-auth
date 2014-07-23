import six


SERIALIZABLE_TYPES = (dict, list, tuple, set, bool, type(None)) + \
                     six.integer_types + six.string_types + \
                     (six.text_type, six.binary_type,)


def partial_to_session(strategy, next, backend, request=None, *args, **kwargs):
    user = kwargs.get('user')
    social = kwargs.get('social')
    clean_kwargs = {
        'response': kwargs.get('response') or {},
        'details': kwargs.get('details') or {},
        'username': kwargs.get('username'),
        'uid': kwargs.get('uid'),
        'is_new': kwargs.get('is_new') or False,
        'new_association': kwargs.get('new_association') or False,
        'user': user and user.id or None,
        'social': social and {
            'provider': social.provider,
            'uid': social.uid
        } or None
    }
    
    kwargs.update(clean_kwargs)

    # Clean any MergeDict data type from the values
    new_kwargs = {}
    for name, value in kwargs.items():
        # Check for class name to avoid importing Django MergeDict or
        # Werkzeug MultiDict
        if isinstance(value, dict) or \
           value.__class__.__name__ in ('MergeDict', 'MultiDict'):
            value = dict(value)
        if isinstance(value, SERIALIZABLE_TYPES):
            new_kwargs[name] = strategy.to_session_value(value)

    return {
        'next': next,
        'backend': backend.name,
        'args': tuple(map(strategy.to_session_value, args)),
        'kwargs': new_kwargs
    }


def partial_from_session(strategy, session):
    kwargs = session['kwargs'].copy()
    user = kwargs.get('user')
    social = kwargs.get('social')
    if isinstance(social, dict):
        kwargs['social'] = strategy.storage.user.get_social_auth(**social)
    if user:
        kwargs['user'] = strategy.storage.user.get_user(user)
    return (
        session['next'],
        session['backend'],
        list(map(strategy.from_session_value, session['args'])),
        dict((key, strategy.from_session_value(val))
                for key, val in kwargs.items())
    )
