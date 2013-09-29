import six
import random
import unittest

from sure import expect

from social.strategies.base import BaseStrategy
from social.storage.base import UserMixin, NonceMixin, AssociationMixin, \
                                CodeMixin, BaseStorage

from social.tests.models import User


class BrokenUser(UserMixin):
    pass


class BrokenAssociation(AssociationMixin):
    pass


class BrokenNonce(NonceMixin):
    pass


class BrokenCode(CodeMixin):
    pass


class BrokenStrategy(BaseStrategy):
    pass


class BrokenStrategyWithSettings(BrokenStrategy):
    def get_setting(self, name):
        raise AttributeError()


class BrokenStorage(BaseStorage):
    pass


class BrokenUserTests(unittest.TestCase):
    def setUp(self):
        self.user = BrokenUser

    def tearDown(self):
        self.user = None

    def test_get_username(self):
        self.user.get_username.when.called_with(User('foobar')).should.throw(
            NotImplementedError, 'Implement in subclass'
        )

    def test_user_model(self):
        self.user.user_model.when.called_with().should.throw(
            NotImplementedError, 'Implement in subclass'
        )

    def test_username_max_length(self):
        self.user.username_max_length.when.called_with().should.throw(
            NotImplementedError, 'Implement in subclass'
        )

    def test_get_user(self):
        self.user.get_user.when.called_with(1).should.throw(
            NotImplementedError, 'Implement in subclass'
        )

    def test_get_social_auth(self):
        self.user.get_social_auth.when.called_with('foo', 1).should.throw(
            NotImplementedError, 'Implement in subclass'
        )

    def test_get_social_auth_for_user(self):
        self.user.get_social_auth_for_user.when.called_with(User('foobar')) \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_create_social_auth(self):
        self.user.create_social_auth.when \
            .called_with(User('foobar'), 1, 'foo') \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_disconnect(self):
        self.user.disconnect\
            .when.called_with(BrokenUser())\
            .should.throw(NotImplementedError, 'Implement in subclass')


class BrokenAssociationTests(unittest.TestCase):
    def setUp(self):
        self.association = BrokenAssociation

    def tearDown(self):
        self.association = None

    def test_store(self):
        self.association.store.when \
            .called_with('http://foobar.com', BrokenAssociation()) \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_get(self):
        self.association.get.when.called_with() \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_remove(self):
        self.association.remove.when.called_with([1, 2, 3]) \
            .should.throw(NotImplementedError, 'Implement in subclass')


class BrokenNonceTests(unittest.TestCase):
    def setUp(self):
        self.nonce = BrokenNonce

    def tearDown(self):
        self.nonce = None

    def test_use(self):
        self.nonce.use.when \
            .called_with('http://foobar.com', 1364951922, 'foobar123') \
            .should.throw(NotImplementedError, 'Implement in subclass')


class BrokenCodeTest(unittest.TestCase):
    def setUp(self):
        self.code = BrokenCode

    def tearDown(self):
        self.code = None

    def test_get_code(self):
        self.code.get_code.when \
            .called_with('foobar') \
            .should.throw(NotImplementedError, 'Implement in subclass')


class BrokenStrategyTests(unittest.TestCase):
    def setUp(self):
        self.strategy = BrokenStrategy(storage=BrokenStorage)

    def tearDown(self):
        self.strategy = None

    def test_redirect(self):
        self.strategy.redirect.when \
            .called_with('http://foobar.com') \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_get_setting(self):
        self.strategy.get_setting.when \
            .called_with('foobar') \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_html(self):
        self.strategy.html.when \
            .called_with('<p>foobar</p>') \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_request_data(self):
        self.strategy.request_data.when \
            .called_with() \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_request_host(self):
        self.strategy.request_host.when \
            .called_with() \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_session_get(self):
        self.strategy.session_get.when \
            .called_with('foobar') \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_session_set(self):
        self.strategy.session_set.when \
            .called_with('foobar', 123) \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_session_pop(self):
        self.strategy.session_pop.when \
            .called_with('foobar') \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_build_absolute_uri(self):
        self.strategy.build_absolute_uri.when \
            .called_with('/foobar') \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_render_html_with_tpl(self):
        self.strategy.render_html.when \
            .called_with('foobar.html', context={}) \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_render_html_with_html(self):
        self.strategy.render_html.when \
            .called_with(html='<p>foobar</p>', context={}) \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_render_html_with_none(self):
        self.strategy.render_html.when \
            .called_with() \
            .should.throw(ValueError, 'Missing template or html parameters')

    def test_is_integrity_error(self):
        self.strategy.storage.is_integrity_error.when \
            .called_with(None) \
            .should.throw(NotImplementedError, 'Implement in subclass')

    def test_random_string(self):
        expect(isinstance(self.strategy.random_string(), six.string_types)) \
                .to.equal(True)

    def test_random_string_without_systemrandom(self):
        def SystemRandom():
            raise NotImplementedError()

        orig_random = getattr(random, 'SystemRandom', None)
        random.SystemRandom = SystemRandom

        strategy = BrokenStrategyWithSettings(storage=BrokenStorage)
        expect(isinstance(strategy.random_string(), six.string_types)) \
                .to.equal(True)
        random.SystemRandom = orig_random
