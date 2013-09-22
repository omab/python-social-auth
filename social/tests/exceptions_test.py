import unittest
from sure import expect

from social.exceptions import SocialAuthBaseException, WrongBackend, \
                              AuthFailed, AuthTokenError, \
                              AuthMissingParameter, AuthStateMissing, \
                              NotAllowedToDisconnect, AuthException, \
                              AuthCanceled, AuthUnknownError, \
                              AuthStateForbidden, AuthAlreadyAssociated, \
                              AuthTokenRevoked


class BaseExceptionTestCase(object):
    def test_exception_message(self):
        try:
            raise self.exception
        except SocialAuthBaseException as err:
            expect(str(err)).to.equal(self.expected_message)


class WrongBackendTest(BaseExceptionTestCase, unittest.TestCase):
    exception = WrongBackend('foobar')
    expected_message = 'Incorrect authentication service "foobar"'


class AuthFailedTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthFailed('foobar', 'wrong_user')
    expected_message = 'Authentication failed: wrong_user'


class AuthFailedDeniedTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthFailed('foobar', 'access_denied')
    expected_message = 'Authentication process was canceled'


class AuthTokenErrorTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthTokenError('foobar', 'Incorrect tokens')
    expected_message = 'Token error: Incorrect tokens'


class AuthMissingParameterTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthMissingParameter('foobar', 'username')
    expected_message = 'Missing needed parameter username'


class AuthStateMissingTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthStateMissing('foobar')
    expected_message = 'Session value state missing.'


class NotAllowedToDisconnectTest(BaseExceptionTestCase, unittest.TestCase):
    exception = NotAllowedToDisconnect()
    expected_message = ''


class AuthExceptionTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthException('foobar', 'message')
    expected_message = 'message'


class AuthCanceledTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthCanceled('foobar')
    expected_message = 'Authentication process canceled'


class AuthUnknownErrorTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthUnknownError('foobar', 'some error')
    expected_message = 'An unknown error happened while ' \
                       'authenticating some error'


class AuthStateForbiddenTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthStateForbidden('foobar')
    expected_message = 'Wrong state parameter given.'


class AuthAlreadyAssociatedTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthAlreadyAssociated('foobar')
    expected_message = ''


class AuthTokenRevokedTest(BaseExceptionTestCase, unittest.TestCase):
    exception = AuthTokenRevoked('foobar')
    expected_message = 'User revoke access to the token'
