import sys
import base64

from social.exceptions import NotAllowedToDisconnect
from social.storage.base import UserMixin, NonceMixin, AssociationMixin, \
                                BaseStorage


class BaseModel(object):
    NEXT_ID = 1
    cache = {}

    @classmethod
    def next_id(cls):
        id = cls.NEXT_ID
        cls.NEXT_ID += 1
        return id

    @classmethod
    def get(cls, key):
        return cls.cache.get(key)

    @classmethod
    def reset_cache(cls):
        cls.cache = {}


class User(BaseModel):
    def __init__(self, username, email=None):
        self.id = User.next_id()
        self.username = username
        self.email = email
        self.password = None
        self.social = []
        self.extra_data = {}

    def set_password(self, password):
        self.password = password

    def save(self):
        User.cache[self.username] = self


class TestUserSocialAuth(UserMixin, BaseModel):
    def __init__(self, user, provider, uid, extra_data=None):
        self.id = TestUserSocialAuth.next_id()
        self.user = user
        self.provider = provider
        self.uid = uid
        self.extra_data = extra_data or {}
        self.user.social.append(self)

    @classmethod
    def changed(cls, user):
        user.save()

    @classmethod
    def get_username(cls, user):
        return user.username

    @classmethod
    def user_model(cls):
        return User

    @classmethod
    def username_max_length(cls):
        return sys.maxint

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        return user.password or len(user.social) > 1

    @classmethod
    def disconnect(cls, name, user, association_id=None):
        if cls.allowed_to_disconnect(user, name, association_id):
            TestUserSocialAuth.cache.pop(association_id, None)
            user.social = [s for s in user.social
                                if association_id and association_id != s.id or
                                   s.provider != name]
        else:
            raise NotAllowedToDisconnect()

    @classmethod
    def user_exists(cls, username):
        return User.cache.get(username) is not None

    @classmethod
    def create_user(cls, username, email=None):
        return User(username=username, email=email)

    @classmethod
    def get_user(cls, pk):
        for username, user in User.cache.items():
            if user.id == pk:
                return user

    @classmethod
    def get_social_auth(cls, provider, uid):
        social_user = TestUserSocialAuth.cache.get(uid)
        if social_user and social_user.provider == provider:
            return social_user

    @classmethod
    def get_social_auth_for_user(cls, user):
        return user.social

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        return TestUserSocialAuth(user=user, provider=provider, uid=uid)


class TestNonce(NonceMixin, BaseModel):
    def __init__(self, server_url, timestamp, salt):
        self.id = TestNonce.next_id()
        self.server_url = server_url
        self.timestamp = timestamp
        self.salt = salt

    @classmethod
    def use(cls, server_url, timestamp, salt):
        nonce = TestNonce(server_url, timestamp, salt)
        TestNonce.cache[server_url] = nonce
        return nonce


class TestAssociation(AssociationMixin, BaseModel):
    def __init__(self, server_url, handle):
        self.id = TestAssociation.next_id()
        self.server_url = server_url
        self.handle = handle

    def save(self):
        TestAssociation.cache[(self.server_url, self.handle)] = self

    @classmethod
    def store(cls, server_url, association):
        assoc = TestAssociation.cache.get((server_url, association.handle))
        if assoc is None:
            assoc = TestAssociation(server_url=server_url,
                                    handle=association.handle)
        assoc.secret = base64.encodestring(association.secret)
        assoc.issued = association.issued
        assoc.lifetime = association.lifetime
        assoc.assoc_type = association.assoc_type
        assoc.save()

    @classmethod
    def get(cls, *args, **kwargs):
        return [TestAssociation.cache.get((kwargs.get('server_url'),
                                  kwargs.get('handle')))]

    @classmethod
    def remove(cls, ids_to_delete):
        assoc = filter(lambda a: a.id in ids_to_delete,
                       TestAssociation.cache.values())
        for a in list(assoc):
            TestAssociation.cache.pop((a.server_url, a.handle), None)


class TestStorage(BaseStorage):
    user = TestUserSocialAuth
    nonce = TestNonce
    association = TestAssociation
