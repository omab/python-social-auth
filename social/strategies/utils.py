from social.utils import module_member
from social.exceptions import MissingBackend
from social.backends.utils import get_backend


# Current strategy getter cache, currently only used by Django to set a method
# to get the current strategy which is latter used by backends get_user()
# method to retrieve the user saved in the session. Backends need an strategy
# to properly access the storage, but Django does not know about that when
# creates the backend instance, this method workarounds the problem.
_current_strategy_getter = None


def get_strategy(backends, strategy, storage, request=None, backend=None,
                 *args, **kwargs):
    if backend:
        Backend = get_backend(backends, backend)
        if not Backend:
            raise MissingBackend(backend)
    else:
        Backend = None
    Strategy = module_member(strategy)
    Storage = module_member(storage)
    return Strategy(Backend, Storage, request, backends=backends,
                    *args, **kwargs)


def set_current_strategy_getter(func):
    global _current_strategy_getter
    _current_strategy_getter = func


def get_current_strategy():
    global _current_strategy_getter
    if _current_strategy_getter is not None:
        return _current_strategy_getter()
