import requests

from sure import expect
from httpretty import HTTPretty

from social.actions import do_disconnect
from social.exceptions import NotAllowedToDisconnect
from social.utils import parse_qs

from social.tests.models import User
from social.tests.actions.actions import BaseActionTest


class DisconnectActionTest(BaseActionTest):
    def test_not_allowed_to_disconnect(self):
        self.do_login()
        user = User.get(self.expected_username)
        do_disconnect.when.called_with(self.strategy, user).should.throw(
            NotAllowedToDisconnect
        )

    def test_disconnect(self):
        self.do_login()
        user = User.get(self.expected_username)
        user.password = 'password'
        do_disconnect(self.strategy, user)
        expect(len(user.social)).to.equal(0)

    def test_disconnect_with_partial_pipeline(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_DISCONNECT_PIPELINE': (
                'social.pipeline.partial.save_status_to_session',
                'social.tests.pipeline.ask_for_password',
                'social.tests.pipeline.set_password',
                'social.pipeline.disconnect.allowed_to_disconnect',
                'social.pipeline.disconnect.get_entries',
                'social.pipeline.disconnect.revoke_tokens',
                'social.pipeline.disconnect.disconnect'
            )
        })
        self.do_login()
        user = User.get(self.expected_username)
        redirect = do_disconnect(self.strategy, user)

        url = self.strategy.build_absolute_uri('/password')
        expect(redirect.url).to.equal(url)
        HTTPretty.register_uri(HTTPretty.GET, redirect.url, status=200,
                               body='foobar')
        HTTPretty.register_uri(HTTPretty.POST, redirect.url, status=200)

        password = 'foobar'
        requests.get(url)
        requests.post(url, data={'password': password})
        data = parse_qs(HTTPretty.last_request.body)
        expect(data['password']).to.equal(password)
        self.strategy.session_set('password', data['password'])

        redirect = do_disconnect(self.strategy, user)
        expect(len(user.social)).to.equal(0)
