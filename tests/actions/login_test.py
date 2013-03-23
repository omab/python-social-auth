from tests.actions.actions_tests import BaseActionTest


class LoginActionTest(BaseActionTest):
    expected_username = 'octocat'

    def test_login(self):
        self.do_login()
