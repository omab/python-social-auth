# -*- coding: utf-8 -*-
"""
BlueBird backend utils tests.

The template tags are tested here.
"""

# Django
from django.contrib.auth.models import User
from django.test import TestCase

# 3rd-party
from social.backends.oauth import OAuthAuth

# Local
from ..templatetags.backend_utils import associated
from ..templatetags.backend_utils import social_backends
from ..views import context


class BaseTestCase(TestCase):

    """Common functionality for TestCases."""

    def setUp(self):
        """Setup common functionality."""
        self.context = context()


class SocialBackendsTest(BaseTestCase):

    """Test TemplateTag social_backends."""

    def test_social_backends(self):
        """Twitter and Facebook are our supported backends for now."""
        bes = social_backends(self.context['available_backends'])
        assert len(bes[0]) == 2
        assert bes[0][0][0] == 'facebook'
        assert bes[0][1][0] == 'twitter'
        assert issubclass(bes[0][0][1], OAuthAuth)
        assert issubclass(bes[0][1][1], OAuthAuth)


class AssociatedBackendsTest(BaseTestCase):

    """Test TemplateTag associated."""

    def test_associated(self):
        """Get the associated backend for a user."""
        user = User.objects.create_user(
            username='jacob1', email='jacob1@ps.net', password='top_secret')
        self.context['user'] = user
        auth_name = 'twitter'
        associated(self.context, self.context['available_backends'][auth_name])
        assert not self.context['association']
        user.social_auth.create(provider=auth_name)
        associated(self.context, self.context['available_backends'][auth_name])
        assert self.context['association'].provider == auth_name
        auth_name = 'facebook'
        associated(self.context, self.context['available_backends'][auth_name])
        assert not self.context['association']
        user.social_auth.create(provider=auth_name)
        associated(self.context, self.context['available_backends'][auth_name])
        assert self.context['association'].provider == auth_name
