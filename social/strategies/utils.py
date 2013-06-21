from social.utils import module_member
from social.backends.utils import get_backend


def get_strategy(backends, strategy, storage, *args, **kwargs):
    request = kwargs.pop('request', None)
    backend = kwargs.pop('backend', None)

    if backend:
        Backend = get_backend(backends, backend)
        if not Backend:
            raise ValueError('Missing backend entry')
    else:
        Backend = None
    Strategy = module_member(strategy)
    Storage = module_member(storage)
    kwargs.setdefault('backends', backends)
    kwargs.setdefault('backend', Backend)
    kwargs.setdefault('storage', Storage)
    kwargs.setdefault('request', request)
    return Strategy(*args, **kwargs)
