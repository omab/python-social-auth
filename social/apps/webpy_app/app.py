from urllib2 import quote

import web

from social.utils import sanitize_redirect, user_is_authenticated, \
                         user_is_active
from social.apps.webpy_app.utils import strategy


urls = (
  '/login/(?P<backend>[^/]+)/', 'auth',
  '/complete/(?P<backend>[^/]+)/', 'complete',
  '/disconnect/(?P<backend>[^/]+)/', 'disconnect',
  '/disconnect/(?P<backend>[^/]+)/(?P<association_id>\d+)/', 'disconnect',
)


class BaseViewClass(object):
    def __init__(self, *args, **kwargs):
        self.session = web.web_session
        method = web.ctx.method == 'POST' and 'post' or 'get'
        self.data = web.input(_method=method)
        super(BaseViewClass, self).__init__(*args, **kwargs)

    def get_current_user(self):
        if not hasattr(self, '_user'):
            if self.session.get('logged_in'):
                self._user = self.strategy.get_user(
                    self.session.get('user_id')
                )
            else:
                self._user = None
        return self._user

    def login_user(self, user):
        self.session['logged_in'] = True
        self.session['user_id'] = user.id


class auth(BaseViewClass):
    def GET(self, backend):
        return self._auth(backend)

    def POST(self, backend):
        return self._auth(backend)

    @strategy('/complete/%(backend)s/')
    def _auth(self, backend):
        # Save any defined next value into session
        strategy = self.strategy
        if 'next' in self.data:
            # Check and sanitize a user-defined GET/POST next field value
            redirect_uri = self.data['next']
            if strategy.setting('SANITIZE_REDIRECTS', True):
                redirect_uri = sanitize_redirect(web.ctx.host, redirect_uri)
            self.session['next'] = redirect_uri or \
                                   strategy.setting('LOGIN_REDIRECT_URL')
        return strategy.start()


class complete(BaseViewClass):
    def GET(self, backend, *args, **kwargs):
        return self._complete(backend, *args, **kwargs)

    def POST(self, backend, *args, **kwargs):
        return self._complete(backend, *args, **kwargs)

    @strategy('/complete/%(backend)s/')
    def _complete(self, backend, *args, **kwargs):
        strategy = self.strategy
        # pop redirect value before the session is trashed on login()
        redirect_value = self.session.get('next', '') or \
                         self.data.get('next', '')
        url = strategy.setting('LOGIN_REDIRECT_URL')

        user = self.get_current_user()
        is_authenticated = user_is_authenticated(user)
        if not is_authenticated:
            user = None

        if self.session.get('partial_pipeline'):
            data = self.session.pop('partial_pipeline')
            kwargs = kwargs.copy()
            kwargs.setdefault('user', user)
            idx, xargs, xkwargs = strategy.from_session(data, request=web.ctx,
                                                        *args, **kwargs)

            if xkwargs.get('backend', '') == backend:
                user = strategy.continue_pipeline(pipeline_index=idx,
                                                  *xargs, **xkwargs)
            else:
                strategy.clean_partial_pipeline()
                user = strategy.complete(user=user, request=web.ctx,
                                         *args, **kwargs)
        else:
            user = strategy.complete(user=user, request=web.ctx,
                                     *args, **kwargs)

        if isinstance(user, web.Storage):
            return user

        if is_authenticated:
            if not user:
                url = redirect_value or strategy.setting('LOGIN_REDIRECT_URL')
            else:
                url = redirect_value or \
                      strategy.setting('NEW_ASSOCIATION_REDIRECT_URL') or \
                      strategy.setting('LOGIN_REDIRECT_URL')
        elif user:
            if user_is_active(user):
                # catch is_new flag before login() resets the instance
                is_new = getattr(user, 'is_new', False)
                self.login_user(user)
                # user.social_user is the used UserSocialAuth instance defined
                # in authenticate process
                social_user = user.social_user
                # store last login backend name in session
                self.session['social_auth_last_login_backend'] = \
                        social_user.provider

                # Remove possible redirect URL from session, if this is a new
                # account, send him to the new-users-page if defined.
                new_user_redirect = strategy.setting('NEW_USER_REDIRECT_URL')
                if new_user_redirect and is_new:
                    url = new_user_redirect
                else:
                    url = redirect_value or \
                          strategy.setting('LOGIN_REDIRECT_URL')
            else:
                url = strategy.setting('INACTIVE_USER_URL') or \
                      strategy.setting('LOGIN_ERROR_URL') or \
                      strategy.setting('LOGIN_URL')
        else:
            url = strategy.setting('LOGIN_ERROR_URL') or \
                  strategy.setting('LOGIN_URL')

        if redirect_value and redirect_value != url:
            redirect_value = quote(redirect_value)
            url += ('?' in url and '&' or '?') + \
                   '%s=%s' % ('next', redirect_value)
        return web.seeother(url)


class disconnect(BaseViewClass):
    def GET(self, backend, association_id=None):
        return self._disconnect(backend, association_id)

    def POST(self, backend, association_id=None):
        return self._disconnect(backend, association_id)

    @strategy()
    def _disconnect(self, backend, association_id=None):
        strategy = self.strategy
        user = self.get_current_user()
        strategy.disconnect(user, association_id)
        url = self.data.get('next') or \
              strategy.setting('DISCONNECT_REDIRECT_URL') or \
              strategy.setting('LOGIN_REDIRECT_URL')
        return web.seeother(url)


app_social = web.application(urls, locals())
