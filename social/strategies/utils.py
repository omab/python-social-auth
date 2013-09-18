from social.utils import module_member
from social.backends.utils import get_backend


def get_strategy(backends, strategy, storage, *args, **kwargs):
    backend = kwargs.pop('backend', None)
    request = kwargs.pop('request', None)
    if backend:
        Backend = get_backend(backends, backend)
        if not Backend:
            raise ValueError('Missing backend entry')
    else:
        Backend = None
    Strategy = module_member(strategy)
    Storage = module_member(storage)
    return Strategy(Backend, Storage, request, backends, *args, **kwargs)
