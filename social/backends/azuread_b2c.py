import base64
import json

from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from jwt import DecodeError, ExpiredSignature, decode as jwt_decode

from ..exceptions import AuthTokenError
from .azuread import AzureADOAuth2



import argparse
import base64
import six
import struct

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import requests

# arg_parser = argparse.ArgumentParser(
#     description='JWK to PEM conversion tool')
# arg_parser.add_argument('--org',
#                         dest='org',
#                         help='Domain for Okta org',
#                         required=True)
# args = arg_parser.parse_args()

def intarr2long(arr):
    return int(''.join(["%02x" % byte for byte in arr]), 16)


def base64_to_long(data):
    if isinstance(data, six.text_type):
        data = data.encode("ascii")

    # urlsafe_b64decode will happily convert b64encoded data
    _d = base64.urlsafe_b64decode(bytes(data) + b'==')
    return intarr2long(struct.unpack('%sB' % len(_d), _d))


"""
Copyright (c) 2015 Microsoft Open Technologies, Inc.

All rights reserved.

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
See https://nicksnettravels.builttoroam.com/post/2017/01/24/Verifying-Azure-Active-Directory-JWT-Tokens.aspx
for verifying JWT tokens.
"""

class AzureADB2COAuth2(AzureADOAuth2):
    name = 'azuread-b2c'
    # version = 'v2.0/'
    version = ''
    # https://login.microsoftonline.com/pidevdaveplay1.onmicrosoft.com/oauth2/v2.0/authorize
    OPENID_CONFIGURATION_URL = \
        'https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration'
    # AUTHORIZATION_URL = \
    #     'https://login.microsoftonline.com/{tenant_id}/oauth2/authorize'
    # ACCESS_TOKEN_URL = 'https://login.microsoftonline.com/{tenant_id}/oauth2/token'

    AUTHORIZATION_URL = \
        'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'
    ACCESS_TOKEN_URL = 'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

    JWKS_URL = 'https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys'

    # def __init__(self, *args, **kwargs):
    #     super(AzureADB2COAuth2, self).__init__(*args, **kwargs)
    #     self.redirect_uri = 'https://easycareacademyrespond4.azurewebsites.net/'

    @property
    def tenant_id(self):
        return self.setting('TENANT_ID', 'common')

    # def access_token_url(self):
    #     return self.access_token_url()

    def openid_configuration_url(self):
        return self.OPENID_CONFIGURATION_URL.format(tenant_id=self.tenant_id) + '?p=b2c_1_signuporin'

    def request_access_token(self, *args, **kwargs):
        response = super(AzureADB2COAuth2, self).request_access_token(*args, **kwargs)
        if 'access_token' not in response:
            response['access_token'] = response['id_token']
        return response

    def authorization_url(self):
        return self.AUTHORIZATION_URL.format(tenant_id=self.tenant_id)

    # def auth_extra_arguments(self):
    #     original = super(AzureADB2COAuth2, self).auth_extra_arguments()
    #
    #     # original.update(self.setting('EXTRA_DATA___OMAR'))
    #
    #     # raise Exception(repr(original))
    #     return original

    def access_token_url(self):
        return self.ACCESS_TOKEN_URL.format(tenant_id=self.tenant_id) + '?p=b2c_1_signuporin'

    def jwks_url(self):
        return self.JWKS_URL.format(tenant_id=self.tenant_id) + '?p=b2c_1_signuporin'

    def get_public_key(self, kid):
        # retrieve keys from jwks_url
        resp = self.request(self.jwks_url(), method='GET')
        resp.raise_for_status()

        # find the proper key for the kid
        for key in resp.json()['keys']:
            if key['kid'] == kid:
                exponent = base64_to_long(key['e'])
                modulus = base64_to_long(key['n'])
                numbers = RSAPublicNumbers(exponent, modulus)
                public_key = numbers.public_key(backend=default_backend())
                pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )

                print 'get_public_key, pem=', pem
                return pem

            #     return '-----BEGIN PUBLIC KEY-----\n' \
            #            '{n}{e}\n' \
            #            '-----END PUBLIC KEY-----'.format(**key)

        raise DecodeError('Cannot find kid={}'.format(kid))

    def _correct_msft_missing_padding(self, base64_string):
        """
        Microsoft decided to remove the padding. Unlike Python, PHP seems to like it (https://www.base64decode.org/).

        Let's do what Stackoverflow suggests: https://stackoverflow.com/a/9807138
        """
        missing_padding = len(base64_string) % 4
        if missing_padding != 0:
            base64_string += b'=' * (4 - missing_padding)

        return base64_string

    def user_data(self, access_token, *args, **kwargs):
        response = kwargs.get('response')
        id_token = response.get('id_token')

        first_part = id_token.split('.', 1)[0]

        first_part_decoded_1 = base64.b64decode(self._correct_msft_missing_padding(first_part))
        first_part_decoded_2 = first_part_decoded_1.decode()

        # decode the JWT header as JSON dict
        jwt_header = json.loads(first_part_decoded_2)

        # get key id and algorithm
        key_id = jwt_header['kid']
        # algorithm = 'RSA'
        algorithm = jwt_header['alg']

        key = self.get_public_key(key_id)

        try:
            # retrieve certificate for key_id
            return jwt_decode(
                id_token,
                key=key,
                # verify=False,
                algorithms=algorithm,
                audience=self.setting('AZUREAD_B2C_KEY')
            )
        except (DecodeError, ExpiredSignature) as error:
            raise AuthTokenError(self, error)
