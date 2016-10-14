# -*- coding: utf-8 -*-
"""BlueBird pipeline tests."""

# Standard Library
from unittest import mock

# Django
from django.contrib.auth.models import User
from django.test import TestCase

# Local
from ..pipeline import require_email


class EmailPipeLinetest(TestCase):

    """Test that if no email is present for a user he is to provide one."""

    def setUp(self):
        """Common setup."""
        self.user = User.objects.create_user(
            username='jacob1', email='', password='top_secret')

    def test_user_has_email(self):
        """The user has an email."""
        self.user.email = 'jd@a.com'
        assert not require_email(pipeline_index=1, strategy=None, details={
        }, user=self.user, is_new=True)

    def test_user_is_not_new(self):
        """Existing user does not get asked for email."""
        assert not require_email(
            pipeline_index=1, strategy=None, details={}, user=None, is_new=False)

    def test_email_in_details(self):
        """An Email is provided in the details."""
        assert not require_email(pipeline_index=1, strategy=None, details={
                                 'email': 'jd@a.com'}, user=None, is_new=True)

    def test_email_in_strategy_request_data(self):
        """An email is provided in the strategies request data."""
        strategy = mock.Mock()
        strategy.request_data.return_value = {'email': 'jd@a.com'}
        assert not require_email(
            pipeline_index=1, strategy=strategy, details={}, user=None, is_new=True)
        assert strategy.request_data.called_once_with()

    def test_no_email_in_strategy_request_data(self):
        """No email is provided in the strategies request data."""
        strategy = mock.Mock()
        strategy.request_data.return_value = {}
        response = require_email(
            pipeline_index=1, strategy=strategy, details={}, user=None, is_new=True)
        assert strategy.request_data.called_once_with()
        assert response.status_code == 302
