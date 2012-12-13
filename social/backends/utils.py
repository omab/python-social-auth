from social.utils import import_module
from social.backends import BaseAuthBackend


# Cache for discovered backends.
BACKENDSCACHE = {}


def load_backends(strategy, force_load=False):
    """
    Entry point to the BACKENDS cache. If BACKENDSCACHE hasn't been
    populated, each of the modules referenced in
    AUTHENTICATION_BACKENDS is imported and checked for a BACKENDS
    definition and if enabled, added to the cache.

    Previously all backends were attempted to be loaded at
    import time of this module, which meant that backends that subclass
    bases found in this module would not have the chance to be loaded
    by the time they were added to this module's BACKENDS dict. See:
    https://github.com/omab/django-social-auth/issues/204

    This new approach ensures that backends are allowed to subclass from
    bases in this module and still be picked up.

    A force_load boolean arg is also provided so that get_backend
    below can retry a requested backend that may not yet be discovered.
    """
    if not BACKENDSCACHE or force_load:
        for auth_backend in strategy.setting('AUTHENTICATION_BACKENDS', []):
            mod, cls_name = auth_backend.rsplit('.', 1)
            module = import_module(mod)
            backend = getattr(module, cls_name)

            if issubclass(backend, BaseAuthBackend):
                name = backend.name
                backends = getattr(module, 'BACKENDS', {})
                if name in backends and backends[name].enabled():
                    BACKENDSCACHE[name] = backends[name]
    return BACKENDSCACHE


def get_backend(strategy, name, *args, **kwargs):
    """Returns a backend by name. Backends are stored in the BACKENDSCACHE
    cache dict. If not found, each of the modules referenced in
    AUTHENTICATION_BACKENDS is imported and checked for a BACKENDS
    definition. If the named backend is found in the module's BACKENDS
    definition, it's then stored in the cache for future access.
    """
    try:
        # Cached backend which has previously been discovered
        return BACKENDSCACHE[name]
    except KeyError:
        # Reload BACKENDS to ensure a missing backend hasn't been missed
        load_backends(strategy, force_load=True)
        try:
            return BACKENDSCACHE[name]
        except KeyError:
            return None


def instance_backend(strategy, name, *args, **kwargs):
    backend = get_backend(strategy, name)
    if backend:
        backend = backend(strategy=strategy, *args, **kwargs)
    return backend
