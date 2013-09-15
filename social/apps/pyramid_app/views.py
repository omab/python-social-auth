from pyramid.view import view_config

from social.utils import module_member
from social.actions import do_auth, do_complete, do_disconnect
from social.apps.pyramid_app.utils import strategy, login_required


@view_config(route_name='social.auth', request_method='GET')
@strategy('social.complete')
def auth(request):
    return do_auth(request.strategy, redirect_name='next')


@view_config(route_name='social.complete', request_method=('GET', 'POST'))
@strategy('social.complete')
def complete(request, *args, **kwargs):
    do_login = module_member(request.strategy.setting('LOGIN_FUNCTION'))
    return do_complete(request.strategy, do_login, request.user,
                       redirect_name='next', *args, **kwargs)


@view_config(route_name='social.disconnect', request_method=('POST',))
@view_config(route_name='social.disconnect_association',
             request_method=('POST',))
@strategy()
@login_required
def disconnect(request):
    return do_disconnect(request.strategy, request.user,
                         request.matchdict.get('association_id'),
                         redirect_name='next')
