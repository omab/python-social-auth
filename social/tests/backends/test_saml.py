import re
import json
import sys
import unittest2
import requests
from os import path

from mock import patch
from httpretty import HTTPretty

try:
    from onelogin.saml2.utils import OneLogin_Saml2_Utils
except ImportError:
    # Only available for python 2.7 at the moment, so don't worry if this fails
    pass

from social.tests.backends.base import BaseBackendTest
from social.p3 import urlparse, urlunparse, urlencode, parse_qs

DATA_DIR = path.join(path.dirname(__file__), 'data')


@unittest2.skipUnless(
    sys.version_info[:2] == (2, 7),
    'python-saml currently depends on 2.7; 3+ support coming soon')
@unittest2.skipIf('__pypy__' in sys.builtin_module_names,
                  'dm.xmlsec not compatible with pypy')
class SAMLTest(BaseBackendTest):
    backend_path = 'social.backends.saml.SAMLAuth'
    expected_username = 'myself'

    def extra_settings(self):
        name = path.join(DATA_DIR, 'saml_config.json')
        with open(name, 'r') as config_file:
            config_str = config_file.read()
        return json.loads(config_str)

    def setUp(self):
        """Patch the time so that we can replay canned
        request/response pairs"""
        super(SAMLTest, self).setUp()

        @staticmethod
        def fixed_time():
            return OneLogin_Saml2_Utils.parse_SAML_to_time(
                '2015-05-09T03:57:22Z'
            )
        now_patch = patch.object(OneLogin_Saml2_Utils, 'now', fixed_time)
        now_patch.start()
        self.addCleanup(now_patch.stop)

    def install_http_intercepts(self, start_url, return_url):
        # When we request start_url
        # (https://idp.testshib.org/idp/profile/SAML2/Redirect/SSO...)
        # we will eventually get a redirect back, with SAML assertion
        # data in the query string.  A pre-recorded correct response
        # is kept in this .txt file:
        name = path.join(DATA_DIR, 'saml_response.txt')
        with open(name, 'r') as response_file:
            response_url = response_file.read()
        HTTPretty.register_uri(HTTPretty.GET, start_url, status=301,
                               location=response_url)
        HTTPretty.register_uri(HTTPretty.GET, return_url, status=200,
                               body='foobar')

    def do_start(self):
        # pretend we've started with a URL like /login/saml/?idp=testshib:
        self.strategy.set_request_data({'idp': 'testshib'}, self.backend)
        start_url = self.backend.start().url
        # Modify the start URL to make the SAML request consistent
        # from test to test:
        start_url = self.modify_start_url(start_url)
        # If the SAML Identity Provider recognizes the user, we will
        # be redirected back to:
        return_url = self.backend.redirect_uri
        self.install_http_intercepts(start_url, return_url)
        response = requests.get(start_url)
        self.assertTrue(response.url.startswith(return_url))
        self.assertEqual(response.text, 'foobar')
        query_values = dict((k, v[0]) for k, v in
                            parse_qs(urlparse(response.url).query).items())
        self.assertNotIn(' ', query_values['SAMLResponse'])
        self.strategy.set_request_data(query_values, self.backend)
        return self.backend.complete()

    def test_metadata_generation(self):
        """Test that we can generate the metadata without error"""
        xml, errors = self.backend.generate_metadata_xml()
        self.assertEqual(len(errors), 0)
        self.assertEqual(xml[0], '<')

    def test_login(self):
        """Test that we can authenticate with a SAML IdP (TestShib)"""
        self.do_login()

    def modify_start_url(self, start_url):
        """
        Given a SAML redirect URL, parse it and change the ID to
        a consistent value, so the request is always identical.
        """
        # Parse the SAML Request URL to get the XML being sent to TestShib
        url_parts = urlparse(start_url)
        query = dict((k, v[0]) for (k, v) in
                     parse_qs(url_parts.query).iteritems())
        xml = OneLogin_Saml2_Utils.decode_base64_and_inflate(
            query['SAMLRequest']
        )
        # Modify the XML:
        xml, changed = re.subn(r'ID="[^"]+"', 'ID="TEST_ID"', xml)
        self.assertEqual(changed, 1)
        # Update the URL to use the modified query string:
        query['SAMLRequest'] = OneLogin_Saml2_Utils.deflate_and_base64_encode(
            xml
        )
        url_parts = list(url_parts)
        url_parts[4] = urlencode(query)
        return urlunparse(url_parts)
