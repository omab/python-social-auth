import unittest

from social.backends.base import BaseAuth


class BrokenBackendAuth(BaseAuth):
    name = 'broken'


class BrokenBackendTest(unittest.TestCase):
    def setUp(self):
        self.backend = BrokenBackendAuth()

    def tearDown(self):
        self.backend = None

    def test_auth_url(self):
        self.backend.auth_url.when.called_with().should.throw(
            NotImplementedError,
            'Implement in subclass'
        )

    def test_auth_html(self):
        self.backend.auth_html.when.called_with().should.throw(
            NotImplementedError,
            'Implement in subclass'
        )

    def test_auth_complete(self):
        self.backend.auth_complete.when.called_with().should.throw(
            NotImplementedError,
            'Implement in subclass'
        )

    def test_get_user_details(self):
        self.backend.get_user_details.when.called_with(None).should.throw(
            NotImplementedError,
            'Implement in subclass'
        )
