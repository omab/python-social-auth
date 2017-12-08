#! /usr/bin/env nix-shell
#! nix-shell -i python -p python27Packages.requests2 -p python27Packages.cryptography

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


# print("Fetching JWKS from {}".format(args.org))
# r = requests.get("https://{}/oauth2/v1/keys".format(args.org))
r = requests.get('https://login.microsoftonline.com/pidevdaveplay1.onmicrosoft.com/discovery/v2.0/keys?p=b2c_1_signuporin')
jwks = r.json()

for jwk in jwks['keys']:
    exponent = base64_to_long(jwk['e'])
    modulus = base64_to_long(jwk['n'])
    numbers = RSAPublicNumbers(exponent, modulus)
    public_key = numbers.public_key(backend=default_backend())
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    print "PEM for KID '{}'".format(jwk['kid'])
    print pem

