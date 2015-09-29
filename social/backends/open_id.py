import datetime
import six
import time
from calendar import timegm

from jwkest import JWKESTException
from jwkest.jwk import KEYS
from jwkest.jws import JWS

from openid.consumer.consumer import Consumer, SUCCESS, CANCEL, FAILURE
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import sreg, ax, pape

from social.utils import url_add_parameters
from social.exceptions import AuthException, AuthFailed, AuthCanceled, \
                              AuthUnknownError, AuthMissingParameter, \
                              AuthTokenError
from social.backends.base import BaseAuth
from social.backends.oauth import BaseOAuth2


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
    URL = None
    USERNAME_KEY = 'username'

    def get_user_id(self, details, response):
        """Return user unique id provided by service"""
        return response.identity_url

    def get_ax_attributes(self):
        attrs = self.setting('AX_SCHEMA_ATTRS', [])
        if attrs and self.setting('IGNORE_DEFAULT_AX_ATTRS', True):
            return attrs
        return attrs + AX_SCHEMA_ATTRS + OLD_AX_ATTRS

    def get_sreg_attributes(self):
        return self.setting('SREG_ATTR') or SREG_ATTR

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
        values.update(self.values_from_response(
            response, self.get_sreg_attributes(), self.get_ax_attributes()
        ))

        fullname = values.get('fullname') or ''
        first_name = values.get('first_name') or ''
        last_name = values.get('last_name') or ''
        email = values.get('email') or ''

        if not fullname and first_name and last_name:
            fullname = first_name + ' ' + last_name
        elif fullname:
            try:
                first_name, last_name = fullname.rsplit(' ', 1)
            except ValueError:
                last_name = fullname

        username_key = self.setting('USERNAME_KEY') or self.USERNAME_KEY
        values.update({'fullname': fullname, 'first_name': first_name,
                       'last_name': last_name,
                       'username': values.get(username_key) or
                                   (first_name.title() + last_name.title()),
                       'email': email})
        return values

    def extra_data(self, user, uid, response, details=None, *args, **kwargs):
        """Return defined extra data names to store in extra_data field.
        Settings will be inspected to get more values names that should be
        stored on extra_data field. Setting name is created from current
        backend name (all uppercase) plus _SREG_EXTRA_DATA and
        _AX_EXTRA_DATA because values can be returned by SimpleRegistration
        or AttributeExchange schemas.

        Both list must be a value name and an alias mapping similar to
        SREG_ATTR, OLD_AX_ATTRS or AX_SCHEMA_ATTRS
        """
        sreg_names = self.setting('SREG_EXTRA_DATA')
        ax_names = self.setting('AX_EXTRA_DATA')
        values = self.values_from_response(response, sreg_names, ax_names)
        from_details = super(OpenIdAuth, self).extra_data(
            user, uid, {}, details, *args, **kwargs
        )
        values.update(from_details)
        return values

    def auth_url(self):
        """Return auth URL returned by service"""
        openid_request = self.setup_request(self.auth_extra_arguments())
        # Construct completion URL, including page we should redirect to
        return_to = self.strategy.absolute_uri(self.redirect_uri)
        return openid_request.redirectURL(self.trust_root(), return_to)

    def auth_html(self):
        """Return auth HTML returned by service"""
        openid_request = self.setup_request(self.auth_extra_arguments())
        return_to = self.strategy.absolute_uri(self.redirect_uri)
        form_tag = {'id': 'openid_message'}
        return openid_request.htmlMarkup(self.trust_root(), return_to,
                                         form_tag_attrs=form_tag)

    def trust_root(self):
        """Return trust-root option"""
        return self.setting('OPENID_TRUST_ROOT') or \
               self.strategy.absolute_uri('/')

    def continue_pipeline(self, *args, **kwargs):
        """Continue previous halted pipeline"""
        response = self.consumer().complete(dict(self.data.items()),
                                            self.strategy.absolute_uri(
                                                self.redirect_uri
                                            ))
        kwargs.update({'response': response, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)

    def auth_complete(self, *args, **kwargs):
        """Complete auth process"""
        response = self.consumer().complete(dict(self.data.items()),
                                            self.strategy.absolute_uri(
                                                self.redirect_uri
                                            ))
        self.process_error(response)
        kwargs.update({'response': response, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)

    def process_error(self, data):
        if not data:
            raise AuthException(self, 'OpenID relying party endpoint')
        elif data.status == FAILURE:
            raise AuthFailed(self, data.message)
        elif data.status == CANCEL:
            raise AuthCanceled(self)
        elif data.status != SUCCESS:
            raise AuthUnknownError(self, data.status)

    def setup_request(self, params=None):
        """Setup request"""
        request = self.openid_request(params)
        # Request some user details. Use attribute exchange if provider
        # advertises support.
        if request.endpoint.supportsType(ax.AXMessage.ns_uri):
            fetch_request = ax.FetchRequest()
            # Mark all attributes as required, Google ignores optional ones
            for attr, alias in self.get_ax_attributes():
                fetch_request.add(ax.AttrInfo(attr, alias=alias,
                                              required=True))
        else:
            fetch_request = sreg.SRegRequest(
                optional=list(dict(self.get_sreg_attributes()).keys())
            )
        request.addExtension(fetch_request)

        # Add PAPE Extension for if configured
        preferred_policies = self.setting(
            'OPENID_PAPE_PREFERRED_AUTH_POLICIES'
        )
        preferred_level_types = self.setting(
            'OPENID_PAPE_PREFERRED_AUTH_LEVEL_TYPES'
        )
        max_age = self.setting('OPENID_PAPE_MAX_AUTH_AGE')
        if max_age is not None:
            try:
                max_age = int(max_age)
            except (ValueError, TypeError):
                max_age = None

        if max_age is not None or preferred_policies or preferred_level_types:
            pape_request = pape.Request(
                max_auth_age=max_age,
                preferred_auth_policies=preferred_policies,
                preferred_auth_level_types=preferred_level_types
            )
            request.addExtension(pape_request)
        return request

    def consumer(self):
        """Create an OpenID Consumer object for the given Django request."""
        if not hasattr(self, '_consumer'):
            self._consumer = self.create_consumer(self.strategy.openid_store())
        return self._consumer

    def create_consumer(self, store=None):
        return Consumer(self.strategy.openid_session_dict(SESSION_NAME), store)

    def uses_redirect(self):
        """Return true if openid request will be handled with redirect or
        HTML content will be returned.
        """
        return self.openid_request().shouldSendRedirect()

    def openid_request(self, params=None):
        """Return openid request"""
        try:
            return self.consumer().begin(url_add_parameters(self.openid_url(),
                                         params))
        except DiscoveryFailure as err:
            raise AuthException(self, 'OpenID discovery error: {0}'.format(
                err
            ))

    def openid_url(self):
        """Return service provider URL.
        This base class is generic accepting a POST parameter that specifies
        provider URL."""
        if self.URL:
            return self.URL
        elif OPENID_ID_FIELD in self.data:
            return self.data[OPENID_ID_FIELD]
        else:
            raise AuthMissingParameter(self, OPENID_ID_FIELD)


class OpenIdConnectAssociation(object):
    """ Use Association model to save the nonce by force. """

    def __init__(self, handle, secret='', issued=0, lifetime=0, assoc_type=''):
        self.handle = handle  # as nonce
        self.secret = secret.encode()  # not use
        self.issued = issued  # not use
        self.lifetime = lifetime  # not use
        self.assoc_type = assoc_type  # as state


class _cache(object):
    """
    Cache decorator that caches the return value of a method for a specified time.

    It maintains a cache per class, so subclasses have a different cache entry
    for the same cached method.

    Does not work for methods with arguments.
    """
    def __init__(self, ttl):
        self.ttl = ttl
        self.cache = {}

    def __call__(self, fn):
        def wrapped(this):
            now = time.time()
            last_updated = None
            cached_value = None
            if this.__class__ in self.cache:
                last_updated, cached_value = self.cache[this.__class__]
            if not cached_value or now - last_updated > self.ttl:
                cached_value = fn(this)
                self.cache[this.__class__] = (now, cached_value)
            return cached_value
        return wrapped


def _autoconf(name):
    """
    fget helper function to fetch the value of a property from the OIDC
    configuration
    """
    def getter(self):
        return self.oidc_config().get(name)
    return getter


class OpenIdConnectAuth(BaseOAuth2):
    """
    Base class for Open ID Connect backends.

    Currently only the code response type is supported.
    """
    # Override OIDC_ENDPOINT in your subclass to enable autoconfig of OIDC
    OIDC_ENDPOINT = None

    DEFAULT_SCOPE = ['openid', 'profile', 'email']
    EXTRA_DATA = ['id_token', 'refresh_token', ('sub', 'id')]
    REDIRECT_STATE = False
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_METHOD = 'GET'

    @_cache(ttl=600)
    def oidc_config(self):
        return self.get_json(self.OIDC_ENDPOINT + '/.well-known/openid-configuration')

    ID_TOKEN_ISSUER = property(_autoconf('issuer'))
    ACCESS_TOKEN_URL = property(_autoconf('token_endpoint'))
    AUTHORIZATION_URL = property(_autoconf('authorization_endpoint'))
    REVOKE_TOKEN_URL = property(_autoconf('revocation_endpoint'))
    USERINFO_URL = property(_autoconf('userinfo_endpoint'))
    JWKS_URI = property(_autoconf('jwks_uri'))

    @_cache(ttl=600)
    def get_jwks_keys(self):
        keys = KEYS()
        keys.load_from_url(self.JWKS_URI)

        # Add client secret as oct key so it can be used for HMAC signatures
        _client_id, client_secret = self.get_key_and_secret()
        keys.add({'key': client_secret, 'kty': 'oct'})
        return keys

    def auth_params(self, state=None):
        """Return extra arguments needed on auth process."""
        params = super(OpenIdConnectAuth, self).auth_params(state)
        params['nonce'] = self.get_and_store_nonce(
            self.AUTHORIZATION_URL, state
        )
        return params

    def get_and_store_nonce(self, url, state):
        # Create a nonce
        nonce = self.strategy.random_string(64)
        # Store the nonce
        association = OpenIdConnectAssociation(nonce, assoc_type=state)
        self.strategy.storage.association.store(url, association)
        return nonce

    def get_nonce(self, nonce):
        try:
            return self.strategy.storage.association.get(
                server_url=self.AUTHORIZATION_URL,
                handle=nonce
            )[0]
        except IndexError:
            pass

    def remove_nonce(self, nonce_id):
        self.strategy.storage.association.remove([nonce_id])

    def validate_claims(self, id_token):
        if id_token['iss'] != self.ID_TOKEN_ISSUER:
            raise AuthTokenError(self, 'Token error: Invalid issuer')

        client_id, _client_secret = self.get_key_and_secret()
        if isinstance(id_token['aud'], six.string_types):
            id_token['aud'] = [id_token['aud']]
        if client_id not in id_token['aud']:
            raise AuthTokenError(self, 'Token error: Invalid audience')

        if len(id_token['aud']) > 1 and 'azp' not in id_token:
            raise AuthTokenError(self, 'Incorrect id_token: azp')

        if 'azp' in id_token and id_token['azp'] != client_id:
            raise AuthTokenError(self, 'Incorrect id_token: azp')

        utc_timestamp = timegm(datetime.datetime.utcnow().utctimetuple())
        if utc_timestamp > id_token['exp']:
            raise AuthTokenError(self, 'Token error: Signature has expired')

        if 'nbf' in id_token and utc_timestamp < id_token['nbf']:
            raise AuthTokenError(self, 'Incorrect id_token: nbf')

        # Verify the token was issued in the last 10 minutes
        if utc_timestamp > id_token['iat'] + 600:
            raise AuthTokenError(self, 'Incorrect id_token: iat')

        # Validate the nonce to ensure the request was not modified
        nonce = id_token.get('nonce')
        if not nonce:
            raise AuthTokenError(self, 'Incorrect id_token: nonce')

        nonce_obj = self.get_nonce(nonce)
        if nonce_obj:
            self.remove_nonce(nonce_obj.id)
        else:
            raise AuthTokenError(self, 'Incorrect id_token: nonce')

    def validate_and_return_id_token(self, jws):
        """
        Validates the id_token according to the steps at
        http://openid.net/specs/openid-connect-core-1_0.html#IDTokenValidation.
        """
        try:
            # Decode the JWT and raise an error if the sig is invalid
            id_token = JWS().verify_compact(jws.encode('utf-8'), self.get_jwks_keys())
        except JWKESTException:
            raise AuthTokenError(self, 'Token error: Signature verification failed')

        self.validate_claims(id_token)

        return id_token

    def request_access_token(self, *args, **kwargs):
        """
        Retrieve the access token. Also, validate the id_token and
        store it (temporarily).
        """
        response = self.get_json(*args, **kwargs)
        self.id_token = self.validate_and_return_id_token(response['id_token'])
        return response

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json(self.USERINFO_URL,
                             headers={'Authorization': 'Bearer {0}'.format(access_token)})

    def get_user_details(self, response):
        return {
            'username': response.get('preferred_username'),
            'email': response.get('email'),
            'fullname': response.get('name'),
            'first_name': response.get('given_name'),
            'last_name': response.get('family_name'),
        }
