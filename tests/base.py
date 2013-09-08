import unittest
import requests

from sure import expect
from httpretty import HTTPretty

from social.utils import parse_qs
from social.backends.utils import user_backends_data


class BaseBackendTest(unittest.TestCase):
    def do_start(self):
        raise NotImplementedError('Implement in subclass')

    def do_login(self):
        user = self.do_start()
        username = self.expected_username
        expect(user.username).to.equal(username)
        expect(self.strategy.session_get('username')).to.equal(username)
        expect(self.strategy.get_user(user.id)).to.equal(user)
        expect(self.strategy.backend.get_user(user.id)).to.equal(user)
        user_backends = user_backends_data(
            user,
            self.strategy.get_setting('SOCIAL_AUTH_AUTHENTICATION_BACKENDS'),
            self.strategy.storage
        )
        expect(len(list(user_backends.keys()))).to.equal(3)
        expect('associated' in user_backends).to.equal(True)
        expect('not_associated' in user_backends).to.equal(True)
        expect('backends' in user_backends).to.equal(True)
        expect(len(user_backends['associated'])).to.equal(1)
        expect(len(user_backends['not_associated'])).to.equal(1)
        expect(len(user_backends['backends'])).to.equal(2)
        return user

    def pipeline_settings(self):
        self.strategy.set_settings({
            'SOCIAL_AUTH_PIPELINE': (
                'social.pipeline.social_auth.social_details',
                'social.pipeline.social_auth.social_uid',
                'social.pipeline.social_auth.auth_allowed',
                'social.pipeline.partial.save_status_to_session',
                'tests.pipeline.ask_for_password',
                'tests.pipeline.ask_for_slug',
                'social.pipeline.social_auth.social_user',
                'social.pipeline.user.get_username',
                'social.pipeline.social_auth.associate_by_email',
                'social.pipeline.user.create_user',
                'social.pipeline.social_auth.associate_user',
                'social.pipeline.social_auth.load_extra_data',
                'tests.pipeline.set_password',
                'tests.pipeline.set_slug',
                'social.pipeline.user.user_details'
            )
        })

    def pipeline_handlers(self, url):
        HTTPretty.register_uri(HTTPretty.GET, url, status=200, body='foobar')
        HTTPretty.register_uri(HTTPretty.POST, url, status=200)

    def pipeline_password_handling(self, url):
        password = 'foobar'
        requests.get(url)
        requests.post(url, data={'password': password})

        data = parse_qs(HTTPretty.last_request.body)
        expect(data['password']).to.equal(password)
        self.strategy.session_set('password', data['password'])
        return password

    def pipeline_slug_handling(self, url):
        slug = 'foo-bar'
        requests.get(url)
        requests.post(url, data={'slug': slug})

        data = parse_qs(HTTPretty.last_request.body)
        expect(data['slug']).to.equal(slug)
        self.strategy.session_set('slug', data['slug'])
        return slug

    def do_partial_pipeline(self):
        url = self.strategy.build_absolute_uri('/password')
        self.pipeline_settings()
        redirect = self.do_start()
        expect(redirect.url).to.equal(url)
        self.pipeline_handlers(url)

        password = self.pipeline_password_handling(url)
        data = self.strategy.session_pop('partial_pipeline')
        idx, backend, xargs, xkwargs = self.strategy.from_session(data)
        expect(backend).to.equal(self.backend.name)
        redirect = self.strategy.continue_pipeline(pipeline_index=idx,
                                                   *xargs, **xkwargs)

        url = self.strategy.build_absolute_uri('/slug')
        expect(redirect.url).to.equal(url)
        self.pipeline_handlers(url)
        slug = self.pipeline_slug_handling(url)

        data = self.strategy.session_pop('partial_pipeline')
        idx, backend, xargs, xkwargs = self.strategy.from_session(data)
        expect(backend).to.equal(self.backend.name)
        user = self.strategy.continue_pipeline(pipeline_index=idx,
                                               *xargs, **xkwargs)

        expect(user.username).to.equal(self.expected_username)
        expect(user.slug).to.equal(slug)
        expect(user.password).to.equal(password)
        return user
