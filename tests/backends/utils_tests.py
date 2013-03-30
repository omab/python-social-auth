import unittest
from sure import expect

from tests.models import TestStorage
from tests.strategy import TestStrategy
from social.backends.utils import load_backends, get_backend
from social.backends.github import GithubOAuth2

# social.backends.utils              28     22    21%   27-32, 42-51, 66-76


class BackendUtilsTest(unittest.TestCase):
    def setUp(self):
        self.strategy = TestStrategy(storage=TestStorage)

    def tearDown(self):
        self.strategy = None

    def test_load_backends(self):
        loaded_backends = load_backends((
            'social.backends.github.GithubOAuth2',
            'social.backends.facebook.FacebookOAuth2',
            'social.backends.flickr.FlickrOAuth'
        ))
        keys = list(loaded_backends.keys())
        keys.sort()
        expect(keys).to.equal(['facebook', 'flickr', 'github'])

        backends = ()
        loaded_backends = load_backends(backends, force_load=True)
        expect(len(list(loaded_backends.keys()))).to.equal(0)

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
