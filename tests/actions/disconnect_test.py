from sure import expect

from social.actions import do_disconnect
from social.exceptions import NotAllowedToDisconnect

from tests.models import User
from tests.actions.actions_tests import BaseActionTest


class LoginActionTest(BaseActionTest):
    def test_not_allowed_to_disconnect(self):
        self.do_login()
        user = User.get(self.expected_username)
        self.assertRaises(NotAllowedToDisconnect, do_disconnect,
                          self.strategy, user)

    def test_disconnect(self):
        self.do_login()
        user = User.get(self.expected_username)
        user.password = 'password'
        do_disconnect(self.strategy, user)
        expect(len(user.social)).to.equal(0)
