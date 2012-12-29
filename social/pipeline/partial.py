def save_status_to_session(strategy, pipeline_index, *args, **kwargs):
    """Saves current social-auth status to session."""
    strategy.session_set('partial_pipeline',
                         strategy.to_session(pipeline_index + 1,
                                             *args, **kwargs))
