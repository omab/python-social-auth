from sure import expect

from tests.models import User

from tests.actions.actions_tests import BaseActionTest


class LoginActionTest(BaseActionTest):
    def test_login(self):
        self.do_login()

    def test_login_with_partial_pipeline(self):
        self.do_login_with_partial_pipeline()

    def test_fields_stored_in_session(self):
        self.do_fields_stored_in_session()

    def test_redirect_value(self):
        self.do_redirect_value()

    def test_login_with_invalid_partial_pipeline(self):
        self.do_invalid_pipeline()

    def test_inactive_user(self):
        self.do_inactive_user()

    def test_invalid_user(self):
        self.do_invalidate_user()
