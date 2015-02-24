import datetime
import json

from httpretty import HTTPretty

from social.p3 import urlencode
from social.actions import do_disconnect

from social.tests.models import User
from social.tests.backends.oauth import OAuth1Test, OAuth2Test
from social.tests.backends.open_id import OpenIdTest, OpenIdConnectTestMixin


class GoogleOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.google.GoogleOAuth2'
    user_data_url = 'https://www.googleapis.com/plus/v1/people/me'
    expected_username = 'foo'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    user_data_body = json.dumps({
        'aboutMe': 'About me text',
        'cover': {
            'coverInfo': {
                'leftImageOffset': 0,
                'topImageOffset': 0
            },
            'coverPhoto': {
                'height': 629,
                'url': 'https://lh5.googleusercontent.com/-ui-GqpNh5Ms/'
                       'AAAAAAAAAAI/AAAAAAAAAZw/a7puhHMO_fg/photo.jpg',
                'width': 940
            },
            'layout': 'banner'
        },
        'displayName': 'Foo Bar',
        'emails': [{
            'type': 'account',
            'value': 'foo@bar.com'
        }],
        'etag': '"e-tag string"',
        'gender': 'male',
        'id': '101010101010101010101',
        'image': {
            'url': 'https://lh5.googleusercontent.com/-ui-GqpNh5Ms/'
                   'AAAAAAAAAAI/AAAAAAAAAZw/a7puhHMO_fg/photo.jpg',
        },
        'isPlusUser': True,
        'kind': 'plus#person',
        'language': 'en',
        'name': {
            'familyName': 'Bar',
            'givenName': 'Foo'
        },
        'objectType': 'person',
        'occupation': 'Software developer',
        'organizations': [{
            'name': 'Org name',
            'primary': True,
            'type': 'school'
        }],
        'placesLived': [{
            'primary': True,
            'value': 'Anyplace'
        }],
        'url': 'https://plus.google.com/101010101010101010101',
        'urls': [{
            'label': 'http://foobar.com',
            'type': 'otherProfile',
            'value': 'http://foobar.com',
        }],
        'verified': False
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()

    def test_with_unique_user_id(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID': True,
        })
        self.do_login()


class GoogleOAuth2DeprecatedAPITest(GoogleOAuth2Test):
    user_data_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    user_data_body = json.dumps({
        'family_name': 'Bar',
        'name': 'Foo Bar',
        'picture': 'https://lh5.googleusercontent.com/-ui-GqpNh5Ms/'
                   'AAAAAAAAAAI/AAAAAAAAAZw/a7puhHMO_fg/photo.jpg',
        'locale': 'en',
        'gender': 'male',
        'email': 'foo@bar.com',
        'birthday': '0000-01-22',
        'link': 'https://plus.google.com/101010101010101010101',
        'given_name': 'Foo',
        'id': '101010101010101010101',
        'verified_email': True
    })

    def test_login(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API': True
        })
        self.do_login()

    def test_partial_pipeline(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API': True
        })
        self.do_partial_pipeline()

    def test_with_unique_user_id(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID': True,
            'SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API': True
        })
        self.do_login()


class GoogleOAuth1Test(OAuth1Test):
    backend_path = 'social.backends.google.GoogleOAuth'
    user_data_url = 'https://www.googleapis.com/userinfo/email'
    expected_username = 'foobar'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    request_token_body = urlencode({
        'oauth_token_secret': 'foobar-secret',
        'oauth_token': 'foobar',
        'oauth_callback_confirmed': 'true'
    })
    user_data_body = urlencode({
        'email': 'foobar@gmail.com',
        'isVerified': 'true',
        'id': '101010101010101010101'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()

    def test_with_unique_user_id(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_GOOGLE_OAUTH_USE_UNIQUE_USER_ID': True
        })
        self.do_login()

    def test_with_anonymous_key_and_secret(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_GOOGLE_OAUTH_KEY': None,
            'SOCIAL_AUTH_GOOGLE_OAUTH_SECRET': None
        })
        self.do_login()


JANRAIN_NONCE = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')


class GoogleOpenIdTest(OpenIdTest):
    backend_path = 'social.backends.google.GoogleOpenId'
    expected_username = 'FooBar'
    discovery_body = ''.join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<xrds:XRDS xmlns:xrds="xri://$xrds" xmlns="xri://$xrd*($v*2.0)">',
        '<XRD>',
        '<Service priority="0">',
        '<Type>http://specs.openid.net/auth/2.0/signon</Type>',
        '<Type>http://openid.net/srv/ax/1.0</Type>',
        '<Type>http://specs.openid.net/extensions/ui/1.0/mode/popup</Type>',
        '<Type>http://specs.openid.net/extensions/ui/1.0/icon</Type>',
        '<Type>http://specs.openid.net/extensions/pape/1.0</Type>',
        '<URI>https://www.google.com/accounts/o8/ud</URI>',
        '</Service>',
        '<Service priority="10">',
        '<Type>http://specs.openid.net/auth/2.0/signon</Type>',
        '<Type>http://openid.net/srv/ax/1.0</Type>',
        '<Type>http://specs.openid.net/extensions/ui/1.0/mode/popup</Type>',
        '<Type>http://specs.openid.net/extensions/ui/1.0/icon</Type>',
        '<Type>http://specs.openid.net/extensions/pape/1.0</Type>',
        '<URI>https://www.google.com/accounts/o8/ud?source=mail</URI>',
        '</Service>',
        '<Service priority="10">',
        '<Type>http://specs.openid.net/auth/2.0/signon</Type>',
        '<Type>http://openid.net/srv/ax/1.0</Type>',
        '<Type>http://specs.openid.net/extensions/ui/1.0/mode/popup</Type>',
        '<Type>http://specs.openid.net/extensions/ui/1.0/icon</Type>',
        '<Type>http://specs.openid.net/extensions/pape/1.0</Type>',
        '<URI>https://www.google.com/accounts/o8/ud?source=gmail.com</URI>',
        '</Service>',
        '<Service priority="10">',
        '<Type>http://specs.openid.net/auth/2.0/signon</Type>',
        '<Type>http://openid.net/srv/ax/1.0</Type>',
        '<Type>http://specs.openid.net/extensions/ui/1.0/mode/popup</Type>',
        '<Type>http://specs.openid.net/extensions/ui/1.0/icon</Type>',
        '<Type>http://specs.openid.net/extensions/pape/1.0</Type>',
        '<URI>',
        'https://www.google.com/accounts/o8/ud?source=googlemail.com',
        '</URI>',
        '</Service>',
        '<Service priority="10">',
        '<Type>http://specs.openid.net/auth/2.0/signon</Type>',
        '<Type>http://openid.net/srv/ax/1.0</Type>',
        '<Type>http://specs.openid.net/extensions/ui/1.0/mode/popup</Type>',
        '<Type>http://specs.openid.net/extensions/ui/1.0/icon</Type>',
        '<Type>http://specs.openid.net/extensions/pape/1.0</Type>',
        '<URI>https://www.google.com/accounts/o8/ud?source=profiles</URI>',
        '</Service>',
        '</XRD>',
        '</xrds:XRDS>'
    ])
    server_response = urlencode({
        'janrain_nonce': JANRAIN_NONCE,
        'openid.assoc_handle': 'assoc-handle',
        'openid.claimed_id': 'https://www.google.com/accounts/o8/id?'
                             'id=some-google-id',
        'openid.ext1.mode': 'fetch_response',
        'openid.ext1.type.email': 'http://axschema.org/contact/email',
        'openid.ext1.type.first_name': 'http://axschema.org/namePerson/first',
        'openid.ext1.type.last_name': 'http://axschema.org/namePerson/last',
        'openid.ext1.type.old_email': 'http://schema.openid.net/contact/email',
        'openid.ext1.value.email': 'foo@bar.com',
        'openid.ext1.value.first_name': 'Foo',
        'openid.ext1.value.last_name': 'Bar',
        'openid.ext1.value.old_email': 'foo@bar.com',
        'openid.identity': 'https://www.google.com/accounts/o8/id?'
                           'id=some-google-id',
        'openid.mode': 'id_res',
        'openid.ns': 'http://specs.openid.net/auth/2.0',
        'openid.ns.ext1': 'http://openid.net/srv/ax/1.0',
        'openid.op_endpoint': 'https://www.google.com/accounts/o8/ud',
        'openid.response_nonce': JANRAIN_NONCE + 'by95cT34vX7p9g',
        'openid.return_to': 'http://myapp.com/complete/google/?'
                            'janrain_nonce=' + JANRAIN_NONCE,
        'openid.sig': 'brT2kmu3eCzb1gQ1pbaXdnWioVM=',
        'openid.signed': 'op_endpoint,claimed_id,identity,return_to,'
                         'response_nonce,assoc_handle,ns.ext1,ext1.mode,'
                         'ext1.type.old_email,ext1.value.old_email,'
                         'ext1.type.first_name,ext1.value.first_name,'
                         'ext1.type.last_name,ext1.value.last_name,'
                         'ext1.type.email,ext1.value.email'
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()


class GoogleRevokeTokenTest(GoogleOAuth2Test):
    def test_revoke_token(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_GOOGLE_OAUTH2_REVOKE_TOKENS_ON_DISCONNECT': True
        })
        self.do_login()
        user = User.get(self.expected_username)
        user.password = 'password'
        HTTPretty.register_uri(self._method(self.backend.REVOKE_TOKEN_METHOD),
                               self.backend.REVOKE_TOKEN_URL,
                               status=200)
        do_disconnect(self.backend, user)


class GoogleOpenIdConnectTest(OpenIdConnectTestMixin, GoogleOAuth2Test):
    backend_path = 'social.backends.google.GoogleOpenIdConnect'
    user_data_url = \
        'https://www.googleapis.com/plus/v1/people/me/openIdConnect'
    issuer = "accounts.google.com"
