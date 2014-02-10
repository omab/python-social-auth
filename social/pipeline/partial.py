from functools import wraps


def save_status_to_session(strategy, pipeline_index, *args, **kwargs):
    """Saves current social-auth status to session."""
    strategy.session_set('partial_pipeline',
                         strategy.partial_to_session(pipeline_index + 1,
                                                     *args, **kwargs))


def partial(func):
    @wraps(func)
    def wrapper(strategy, pipeline_index, *args, **kwargs):
        out = func(strategy=strategy, pipeline_index=pipeline_index,
                    *args, **kwargs) or {}
        if not isinstance(out, dict):
            values = strategy.partial_to_session(pipeline_index, *args,
                                                 **kwargs)
            strategy.session_set('partial_pipeline', values)
        return out
    return wrapper
