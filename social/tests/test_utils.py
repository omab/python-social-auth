import sys
import unittest

from mock import Mock
from sure import expect

from social.utils import sanitize_redirect, user_is_authenticated, \
                         user_is_active, slugify, build_absolute_uri, \
                         partial_pipeline_data


PY3 = sys.version_info[0] == 3


class SanitizeRedirectTest(unittest.TestCase):
    def test_none_redirect(self):
        expect(sanitize_redirect('myapp.com', None)).to.equal(None)

    def test_empty_redirect(self):
        expect(sanitize_redirect('myapp.com', '')).to.equal(None)

    def test_dict_redirect(self):
        expect(sanitize_redirect('myapp.com', {})).to.equal(None)

    def test_invalid_redirect(self):
        expect(sanitize_redirect('myapp.com',
                                 {'foo': 'bar'})).to.equal(None)

    def test_wrong_path_redirect(self):
        expect(sanitize_redirect(
            'myapp.com',
            'http://notmyapp.com/path/'
        )).to.equal(None)

    def test_valid_absolute_redirect(self):
        expect(sanitize_redirect(
            'myapp.com',
            'http://myapp.com/path/'
        )).to.equal('http://myapp.com/path/')

    def test_valid_relative_redirect(self):
        expect(sanitize_redirect('myapp.com', '/path/')).to.equal('/path/')


class UserIsAuthenticatedTest(unittest.TestCase):
    def test_user_is_none(self):
        expect(user_is_authenticated(None)).to.equal(False)

    def test_user_is_not_none(self):
        expect(user_is_authenticated(object())).to.equal(True)

    def test_user_has_is_authenticated(self):
        class User(object):
            is_authenticated = True
        expect(user_is_authenticated(User())).to.equal(True)

    def test_user_has_is_authenticated_callable(self):
        class User(object):
            def is_authenticated(self):
                return True
        expect(user_is_authenticated(User())).to.equal(True)


class UserIsActiveTest(unittest.TestCase):
    def test_user_is_none(self):
        expect(user_is_active(None)).to.equal(False)

    def test_user_is_not_none(self):
        expect(user_is_active(object())).to.equal(True)

    def test_user_has_is_active(self):
        class User(object):
            is_active = True
        expect(user_is_active(User())).to.equal(True)

    def test_user_has_is_active_callable(self):
        class User(object):
            def is_active(self):
                return True
        expect(user_is_active(User())).to.equal(True)


class SlugifyTest(unittest.TestCase):
    def test_slugify_formats(self):
        if PY3:
            expect(slugify('FooBar')).to.equal('foobar')
            expect(slugify('Foo Bar')).to.equal('foo-bar')
            expect(slugify('Foo (Bar)')).to.equal('foo-bar')
        else:
            expect(slugify('FooBar'.decode('utf-8'))).to.equal('foobar')
            expect(slugify('Foo Bar'.decode('utf-8'))).to.equal('foo-bar')
            expect(slugify('Foo (Bar)'.decode('utf-8'))).to.equal('foo-bar')


class BuildAbsoluteURITest(unittest.TestCase):
    def setUp(self):
        self.host = 'http://foobar.com'

    def tearDown(self):
        self.host = None

    def test_path_none(self):
        expect(build_absolute_uri(self.host)).to.equal(self.host)

    def test_path_empty(self):
        expect(build_absolute_uri(self.host, '')).to.equal(self.host)

    def test_path_http(self):
        expect(build_absolute_uri(self.host, 'http://barfoo.com')) \
              .to.equal('http://barfoo.com')

    def test_path_https(self):
        expect(build_absolute_uri(self.host, 'https://barfoo.com')) \
              .to.equal('https://barfoo.com')

    def test_host_ends_with_slash_and_path_starts_with_slash(self):
        expect(build_absolute_uri(self.host + '/', '/foo/bar')) \
              .to.equal('http://foobar.com/foo/bar')

    def test_absolute_uri(self):
        expect(build_absolute_uri(self.host, '/foo/bar')) \
              .to.equal('http://foobar.com/foo/bar')


class PartialPipelineData(unittest.TestCase):
    def test_kwargs_included_in_result(self):
        strategy = self._strategy()
        kwargitem = ('foo', 'bar')
        _, xkwargs = partial_pipeline_data(strategy, None,
                                           *(), **dict([kwargitem]))
        xkwargs.should.have.key(kwargitem[0]).being.equal(kwargitem[1])

    def test_update_user(self):
        user = object()
        strategy = self._strategy(session_kwargs={'user': None})
        _, xkwargs = partial_pipeline_data(strategy, user)
        xkwargs.should.have.key('user').being.equal(user)

    def _strategy(self, session_kwargs=None):
        backend = Mock()
        backend.name = 'mock-backend'

        strategy = Mock()
        strategy.request = None
        strategy.backend = backend
        strategy.session_get.return_value = object()
        strategy.partial_from_session.return_value = \
            (0, backend.name, [], session_kwargs or {})
        return strategy
