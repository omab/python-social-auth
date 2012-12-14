from openid.consumer.consumer import Consumer, SUCCESS, CANCEL, FAILURE
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import sreg, ax, pape

from social.utils import url_add_parameters
from social.exceptions import AuthException, AuthFailed, AuthCanceled, \
                              AuthUnknownError, AuthMissingParameter
from social.backends.base import BaseAuth


# OpenID configuration
OLD_AX_ATTRS = [
    ('http://schema.openid.net/contact/email', 'old_email'),
    ('http://schema.openid.net/namePerson', 'old_fullname'),
    ('http://schema.openid.net/namePerson/friendly', 'old_nickname')
]
AX_SCHEMA_ATTRS = [
    # Request both the full name and first/last components since some
    # providers offer one but not the other.
    ('http://axschema.org/contact/email', 'email'),
    ('http://axschema.org/namePerson', 'fullname'),
    ('http://axschema.org/namePerson/first', 'first_name'),
    ('http://axschema.org/namePerson/last', 'last_name'),
    ('http://axschema.org/namePerson/friendly', 'nickname'),
]
SREG_ATTR = [
    ('email', 'email'),
    ('fullname', 'fullname'),
    ('nickname', 'nickname')
]
OPENID_ID_FIELD = 'openid_identifier'
SESSION_NAME = 'openid'


class OpenIdAuth(BaseAuth):
    """Generic OpenID authentication backend"""
    name = 'openid'

    def get_user_id(self, details, response):
        """Return user unique id provided by service"""
        return response.identity_url

    def values_from_response(self, response, sreg_names=None, ax_names=None):
        """Return values from SimpleRegistration response or
        AttributeExchange response if present.

        @sreg_names and @ax_names must be a list of name and aliases
        for such name. The alias will be used as mapping key.
        """
        values = {}

        # Use Simple Registration attributes if provided
        if sreg_names:
            resp = sreg.SRegResponse.fromSuccessResponse(response)
            if resp:
                values.update((alias, resp.get(name) or '')
                                    for name, alias in sreg_names)

        # Use Attribute Exchange attributes if provided
        if ax_names:
            resp = ax.FetchResponse.fromSuccessResponse(response)
            if resp:
                for src, alias in ax_names:
                    name = alias.replace('old_', '')
                    values[name] = resp.getSingle(src, '') or values.get(name)
        return values

    def get_user_details(self, response):
        """Return user details from an OpenID request"""
        values = {'username': '', 'email': '', 'fullname': '',
                  'first_name': '', 'last_name': ''}
        # update values using SimpleRegistration or AttributeExchange
        # values
        values.update(self.values_from_response(response,
                                                SREG_ATTR,
                                                OLD_AX_ATTRS +
                                                AX_SCHEMA_ATTRS))

        fullname = values.get('fullname') or ''
        first_name = values.get('first_name') or ''
        last_name = values.get('last_name') or ''

        if not fullname and first_name and last_name:
            fullname = first_name + ' ' + last_name
        elif fullname:
            try:
                first_name, last_name = fullname.rsplit(' ', 1)
            except ValueError:
                last_name = fullname

        values.update({'fullname': fullname, 'first_name': first_name,
                       'last_name': last_name,
                       'username': values.get('username') or
                                   (first_name.title() + last_name.title())})
        return values

    def extra_data(self, user, uid, response, details):
        """Return defined extra data names to store in extra_data field.
        Settings will be inspected to get more values names that should be
        stored on extra_data field. Setting name is created from current
        backend name (all uppercase) plus _SREG_EXTRA_DATA and
        _AX_EXTRA_DATA because values can be returned by SimpleRegistration
        or AttributeExchange schemas.

        Both list must be a value name and an alias mapping similar to
        SREG_ATTR, OLD_AX_ATTRS or AX_SCHEMA_ATTRS
        """
        sreg_names = self.strategy.setting('SREG_EXTRA_DATA')
        ax_names = self.strategy.setting('AX_EXTRA_DATA')
        return self.values_from_response(response, sreg_names, ax_names)

    def auth_url(self):
        """Return auth URL returned by service"""
        openid_request = self.setup_request(self.auth_extra_arguments())
        # Construct completion URL, including page we should redirect to
        return_to = self.strategy.build_absolute_uri(self.redirect_uri)
        return openid_request.redirectURL(self.trust_root(), return_to)

    def auth_html(self):
        """Return auth HTML returned by service"""
        openid_request = self.setup_request(self.auth_extra_arguments())
        return_to = self.strategy.build_absolute_uri(self.redirect_uri)
        form_tag = {'id': 'openid_message'}
        return openid_request.htmlMarkup(self.trust_root(), return_to,
                                         form_tag_attrs=form_tag)

    def trust_root(self):
        """Return trust-root option"""
        return self.strategy.setting('OPENID_TRUST_ROOT') or \
               self.strategy.build_absolute_uri('/')

    def continue_pipeline(self, *args, **kwargs):
        """Continue previous halted pipeline"""
        response = self.consumer().complete(dict(self.data.items()),
                                            self.strategy.build_absolute_uri())
        kwargs.update({'response': response, 'backend': self.name})
        return self.strategy.authenticate(*args, **kwargs)

    def auth_complete(self, *args, **kwargs):
        """Complete auth process"""
        response = self.consumer().complete(dict(self.data.items()),
                                            self.strategy.build_absolute_uri())
        if not response:
            raise AuthException(self, 'OpenID relying party endpoint')
        elif response.status == SUCCESS:
            kwargs.update({'response': response, 'backend': self.name})
            return self.strategy.authenticate(*args, **kwargs)
        elif response.status == FAILURE:
            raise AuthFailed(self, response.message)
        elif response.status == CANCEL:
            raise AuthCanceled(self)
        else:
            raise AuthUnknownError(self, response.status)

    def setup_request(self, extra_params=None):
        """Setup request"""
        openid_request = self.openid_request(extra_params)
        # Request some user details. Use attribute exchange if provider
        # advertises support.
        if openid_request.endpoint.supportsType(ax.AXMessage.ns_uri):
            fetch_request = ax.FetchRequest()
            # Mark all attributes as required, Google ignores optional ones
            for attr, alias in (AX_SCHEMA_ATTRS + OLD_AX_ATTRS):
                fetch_request.add(ax.AttrInfo(attr, alias=alias,
                                              required=True))
        else:
            fetch_request = sreg.SRegRequest(optional=dict(SREG_ATTR).keys())
        openid_request.addExtension(fetch_request)

        # Add PAPE Extension for if configured
        preferred_policies = self.strategy.setting(
            'OPENID_PAPE_PREFERRED_AUTH_POLICIES'
        )
        preferred_level_types = self.strategy.setting(
            'OPENID_PAPE_PREFERRED_AUTH_LEVEL_TYPES'
        )
        max_age = self.strategy.setting('OPENID_PAPE_MAX_AUTH_AGE')
        if max_age is not None:
            try:
                max_age = int(max_age)
            except (ValueError, TypeError):
                max_age = None

        if any((max_age, preferred_policies, preferred_level_types)):
            pape_request = pape.Request(
                max_auth_age=max_age,
                preferred_auth_policies=preferred_policies,
                preferred_auth_level_types=preferred_level_types
            )
            openid_request.addExtension(pape_request)
        return openid_request

    def consumer(self):
        """Create an OpenID Consumer object for the given Django request."""
        return Consumer(self.strategy.session_setdefault(SESSION_NAME, {}),
                        self.strategy.openid_store())

    def uses_redirect(self):
        """Return true if openid request will be handled with redirect or
        HTML content will be returned.
        """
        return self.openid_request().shouldSendRedirect()

    def openid_request(self, extra_params=None):
        """Return openid request"""
        if not hasattr(self, '_openid_request'):
            try:
                self._openid_request = self.consumer().begin(
                    url_add_parameters(self.openid_url(), extra_params)
                )
            except DiscoveryFailure, err:
                raise AuthException(self, 'OpenID discovery error: %s' % err)
        return self._openid_request

    def openid_url(self):
        """Return service provider URL.
        This base class is generic accepting a POST parameter that specifies
        provider URL."""
        if OPENID_ID_FIELD not in self.data:
            raise AuthMissingParameter(self, OPENID_ID_FIELD)
        return self.data[OPENID_ID_FIELD]


BACKENDS = {
    'openid': OpenIdAuth
}
