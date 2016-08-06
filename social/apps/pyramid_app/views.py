from pyramid.view import view_config

from social.utils import module_member
from social.actions import do_auth, do_complete, do_disconnect
from social.apps.pyramid_app.utils import psa, login_required


@view_config(route_name='social.auth', request_method=('GET', 'POST'))
@psa('social.complete')
def auth(request):
    return do_auth(request.backend, redirect_name='next')


@view_config(route_name='social.complete', request_method=('GET', 'POST'))
@psa('social.complete')
def complete(request, *args, **kwargs):
    do_login = module_member(request.backend.setting('LOGIN_FUNCTION'))
    return do_complete(request.backend, do_login, request.user,
                       redirect_name='next', *args, **kwargs)


@view_config(route_name='social.disconnect', request_method=('POST',))
@view_config(route_name='social.disconnect_association',
             request_method=('POST',))
@psa()
@login_required
def disconnect(request):
    return do_disconnect(request.backend, request.user,
                         request.matchdict.get('association_id'),
                         redirect_name='next')
