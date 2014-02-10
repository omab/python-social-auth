# -*- coding: utf-8 -*-
import six

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.http import urlquote

from social.exceptions import SocialAuthBaseException


class SocialAuthExceptionMiddleware(object):
    """Middleware that handles Social Auth AuthExceptions by providing the user
    with a message, logging an error, and redirecting to some next location.

    By default, the exception message itself is sent to the user and they are
    redirected to the location specified in the SOCIAL_AUTH_LOGIN_ERROR_URL
    setting.

    This middleware can be extended by overriding the get_message or
    get_redirect_uri methods, which each accept request and exception.
    """
    def process_exception(self, request, exception):
        self.strategy = getattr(request, 'social_strategy', None)
        if self.strategy is None or self.raise_exception(request, exception):
            return

        if isinstance(exception, SocialAuthBaseException):
            backend_name = self.strategy.backend.name
            message = self.get_message(request, exception)
            url = self.get_redirect_uri(request, exception)

            if request.user.is_authenticated():
                # Ensure that messages are added to authenticated users only,
                # otherwise this fails
                messages.error(request, message,
                               extra_tags='social-auth ' + backend_name)
            else:
                url += ('?' in url and '&' or '?') + \
                       'message={0}&backend={1}'.format(urlquote(message),
                                                        backend_name)
            return redirect(url)

    def raise_exception(self, request, exception):
        return self.strategy.setting('RAISE_EXCEPTIONS', settings.DEBUG)

    def get_message(self, request, exception):
        return six.text_type(exception)

    def get_redirect_uri(self, request, exception):
        return self.strategy.setting('LOGIN_ERROR_URL')
