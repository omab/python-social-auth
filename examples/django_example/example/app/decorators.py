from functools import wraps

from django.template import RequestContext
from django.shortcuts import render_to_response


def render_to(tpl):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            out = func(request, *args, **kwargs)
            if isinstance(out, dict):
                out = render_to_response(tpl, out, RequestContext(request))
            return out
        return wrapper
    return decorator
