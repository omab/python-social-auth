"""
Base backends classes.

This module defines base classes needed to define custom OpenID or OAuth1/2
auth services from third parties. This customs must subclass an Auth and a
Backend class, check current implementation for examples.

Also the modules *must* define a BACKENDS dictionary with the backend name
(which is used for URLs matching) and Auth class, otherwise it won't be
enabled.
"""
from requests import request

from social.utils import module_member, parse_qs


class BaseAuth(object):
    """A django.contrib.auth backend that authenticates the user based on
    a authentication provider response"""
    name = ''  # provider name, it's stored in database
    supports_inactive_user = False  # Django auth
    ID_KEY = None

    def __init__(self, strategy=None, redirect_uri=None, *args, **kwargs):
        self.strategy = strategy
        self.redirect_uri = redirect_uri
        self.data = {}
        if strategy:
            self.data = self.strategy.request_data()
            self.redirect_uri = self.strategy.build_absolute_uri(
                self.redirect_uri
            )

    def setting(self, name, default=None):
        """Return setting value from strategy"""
        return self.strategy.setting(name, default)

    def auth_url(self):
        """Must return redirect URL to auth provider"""
        raise NotImplementedError('Implement in subclass')

    def auth_html(self):
        """Must return login HTML content returned by provider"""
        raise NotImplementedError('Implement in subclass')

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        raise NotImplementedError('Implement in subclass')

    def authenticate(self, *args, **kwargs):
        """Authenticate user using social credentials

        Authentication is made if this is the correct backend, backend
        verification is made by kwargs inspection for current backend
        name presence.
        """
        # Validate backend and arguments. Require that the Social Auth
        # response be passed in as a keyword argument, to make sure we
        # don't match the username/password calling conventions of
        # authenticate.
        if 'backend' not in kwargs or kwargs['backend'].name != self.name or \
           'strategy' not in kwargs or 'response' not in kwargs:
            return None

        self.strategy = self.strategy or kwargs.get('strategy')
        self.redirect_uri = self.redirect_uri or kwargs.get('redirect_uri')
        self.data = self.strategy.request_data()
        pipeline = self.strategy.get_pipeline()

        if 'pipeline_index' in kwargs:
            return self.pipeline(pipeline[kwargs['pipeline_index']:],
                                 *args, **kwargs)
        else:
            details = self.get_user_details(kwargs['response'])
            uid = self.get_user_id(details, kwargs['response'])
            return self.pipeline(pipeline, details=details, uid=uid,
                                 is_new=False, *args, **kwargs)

    def pipeline(self, pipeline, pipeline_index=0, *args, **kwargs):
        kwargs['strategy'] = self.strategy

        out = kwargs.copy()
        out.pop(self.name, None)

        for idx, name in enumerate(pipeline):
            out['pipeline_index'] = pipeline_index + idx
            func = module_member(name)
            result = func(*args, **out) or {}
            if not isinstance(result, dict):
                return result
            out.update(result)
        user = out['user']
        if user:
            user.social_user = out['social']
            user.is_new = out['is_new']
        return user

    def extra_data(self, user, uid, response, details):
        """Return default blank user extra data"""
        return {}

    def get_user_id(self, details, response):
        """Must return a unique ID from values returned on details"""
        return response.get(self.ID_KEY)

    def get_user_details(self, response):
        """Must return user details in a know internal struct:
            {'username': <username if any>,
             'email': <user email if any>,
             'fullname': <user full name if any>,
             'first_name': <user first name if any>,
             'last_name': <user last name if any>}
        """
        raise NotImplementedError('Implement in subclass')

    def get_user(self, user_id):
        """
        Return user with given ID from the User model used by this backend.
        This is called by django.contrib.auth.middleware.
        """
        return self.strategy.get_user(user_id)

    def continue_pipeline(self, *args, **kwargs):
        """Continue previous halted pipeline"""
        kwargs.update({'backend': self})
        return self.strategy.authenticate(*args, **kwargs)

    def request_token_extra_arguments(self):
        """Return extra arguments needed on request-token process"""
        return self.setting('REQUEST_TOKEN_EXTRA_ARGUMENTS', {})

    def auth_extra_arguments(self):
        """Return extra arguments needed on auth process. The defaults can be
        overriden by GET parameters."""
        extra_arguments = self.setting('AUTH_EXTRA_ARGUMENTS', {})
        extra_arguments.update((key, self.data[key]) for key in extra_arguments
                                    if key in self.data)
        return extra_arguments

    def uses_redirect(self):
        """Return True if this provider uses redirect url method,
        otherwise return false."""
        return True

    def request(self, url, method='GET', *args, **kwargs):
        kwargs.setdefault('timeout', self.setting('REQUESTS_TIMEOUT') or
                                     self.setting('URLOPEN_TIMEOUT'))
        response = request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response

    def get_json(self, url, *args, **kwargs):
        return self.request(url, *args, **kwargs).json()

    def get_querystring(self, url, *args, **kwargs):
        return parse_qs(self.request(url, *args, **kwargs).text)

    def get_key_and_secret(self):
        """Return tuple with Consumer Key and Consumer Secret for current
        service provider. Must return (key, secret), order *must* be respected.
        """
        return self.setting('KEY'), self.setting('SECRET')
