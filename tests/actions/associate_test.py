from sure import expect

from tests.actions.actions_tests import BaseActionTest
from tests.models import User


class AssociateActionTest(BaseActionTest):
    expected_username = 'foobar'

    def setUp(self):
        super(AssociateActionTest, self).setUp()
        self.user = User(username='foobar', email='foo@bar.com')

    def test_associate(self):
        self.do_login()
        expect(len(self.user.social)).to.equal(1)
        expect(self.user.social[0].provider).to.equal('github')

    def test_associate_with_partial_pipeline(self):
        self.do_login_with_partial_pipeline()
        expect(len(self.user.social)).to.equal(1)
        expect(self.user.social[0].provider).to.equal('github')
