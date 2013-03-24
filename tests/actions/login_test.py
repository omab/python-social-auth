from tests.actions.actions_tests import BaseActionTest


class LoginActionTest(BaseActionTest):
    expected_username = 'octocat'

    def test_login(self):
        self.do_login()

    def test_login_with_partial_pipeline(self):
        self.do_login_with_partial_pipeline()
