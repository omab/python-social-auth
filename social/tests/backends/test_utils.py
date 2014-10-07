import unittest2 as unittest

from social.tests.models import TestStorage
from social.tests.strategy import TestStrategy
from social.backends.utils import load_backends, get_backend
from social.backends.github import GithubOAuth2
from social.exceptions import MissingBackend


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
        self.assertEqual(keys, ['facebook', 'flickr', 'github'])

        backends = ()
        loaded_backends = load_backends(backends, force_load=True)
        self.assertEqual(len(list(loaded_backends.keys())), 0)


class GetBackendTest(BaseBackendUtilsTest):
    def test_get_backend(self):
        backend = get_backend((
            'social.backends.github.GithubOAuth2',
            'social.backends.facebook.FacebookOAuth2',
            'social.backends.flickr.FlickrOAuth'
        ), 'github')
        self.assertEqual(backend, GithubOAuth2)

    def test_get_missing_backend(self):
        with self.assertRaisesRegexp(MissingBackend,
                                     'Missing backend "foobar" entry'):
            get_backend(('social.backends.github.GithubOAuth2',
                         'social.backends.facebook.FacebookOAuth2',
                         'social.backends.flickr.FlickrOAuth'),
                        'foobar')
