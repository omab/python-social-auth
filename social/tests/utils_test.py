import sys
import unittest

from sure import expect

from social.utils import sanitize_redirect, user_is_authenticated, \
                         user_is_active, slugify


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
