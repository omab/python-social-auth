from django.shortcuts import redirect

from social.pipeline.partial import partial


@partial
def require_email(strategy, details, *args, **kwargs):
    if not details.get('email'):
        if strategy.session_get('saved_email'):
            details['email'] = strategy.session_pop('saved_email')
        else:
            return redirect('require_email')
