import time

try:
    import cPickle as pickle
except ImportError:
    import pickle

from openid.store.interface import OpenIDStore as BaseOpenIDStore
from openid.store.nonce import SKEW


class OpenIdStore(BaseOpenIDStore):
    """Storage class"""
    def __init__(self, strategy):
        """Init method"""
        super(OpenIdStore, self).__init__()
        self.strategy = strategy
        self.storage = strategy.storage
        self.assoc = self.storage.association
        self.nonce = self.storage.nonce
        self.max_nonce_age = 6 * 60 * 60  # Six hours

    def storeAssociation(self, server_url, association):
        """Store new assocition if doesn't exist"""
        self.assoc.store(server_url, association)

    def removeAssociation(self, server_url, handle):
        """Remove association"""
        associations_ids = list(dict(self.assoc.oids(server_url,
                                                     handle)).keys())
        if associations_ids:
            self.assoc.remove(associations_ids)

    def getAssociation(self, server_url, handle=None):
        """Return stored assocition"""
        oid_associations = self.assoc.oids(server_url, handle)
        associations = [association
                        for assoc_id, association in oid_associations
                        if association.getExpiresIn() > 0]
        expired = [assoc_id for assoc_id, association in oid_associations
                   if association.getExpiresIn() == 0]

        if expired:  # clear expired associations
            self.assoc.remove(expired)

        if associations:  # return most recet association
            return associations[0]

    def useNonce(self, server_url, timestamp, salt):
        """Generate one use number and return *if* it was created"""
        if abs(timestamp - time.time()) > SKEW:
            return False
        return self.nonce.use(server_url, timestamp, salt)


class OpenIdSessionWrapper(dict):
    pickle_instances = (
        '_yadis_services__openid_consumer_',
        '_openid_consumer_last_token'
    )

    def __getitem__(self, name):
        value = super(OpenIdSessionWrapper, self).__getitem__(name)
        if name in self.pickle_instances:
            value = pickle.loads(value)
        return value

    def __setitem__(self, name, value):
        if name in self.pickle_instances:
            value = pickle.dumps(value, 0)
        super(OpenIdSessionWrapper, self).__setitem__(name, value)

    def get(self, name, default=None):
        try:
            return self[name]
        except KeyError:
            return default
