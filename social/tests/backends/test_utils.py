import unittest
from sure import expect

from social.tests.models import TestStorage
from social.tests.strategy import TestStrategy
from social.backends.utils import load_backends, get_backend
from social.backends.github import GithubOAuth2


class BaseBackendUtilsTest(unittest.TestCase):
    def setUp(self):
        self.strategy = TestStrategy(storage=TestStorage)

    def tearDown(self):
        self.strategy = None


class LoadBackendsTest(BaseBackendUtilsTest):
    def test_load_backends(self):
        loaded_backends = load_backends((
            'social.backends.github.GithubOAuth2',
            'social.backends.facebook.FacebookOAuth2',
            'social.backends.flickr.FlickrOAuth'
        ), force_load=True)
        keys = list(loaded_backends.keys())
        keys.sort()
        expect(keys).to.equal(['facebook', 'flickr', 'github'])

        backends = ()
        loaded_backends = load_backends(backends, force_load=True)
        expect(len(list(loaded_backends.keys()))).to.equal(0)


class GetBackendTest(BaseBackendUtilsTest):
    def test_get_backend(self):
        backend = get_backend((
            'social.backends.github.GithubOAuth2',
            'social.backends.facebook.FacebookOAuth2',
            'social.backends.flickr.FlickrOAuth'
        ), 'github')
        expect(backend).to.equal(GithubOAuth2)

    def test_get_missing_backend(self):
        backend = get_backend((
            'social.backends.github.GithubOAuth2',
            'social.backends.facebook.FacebookOAuth2',
            'social.backends.flickr.FlickrOAuth'
        ), 'foobar')
        expect(backend).to.equal(None)
