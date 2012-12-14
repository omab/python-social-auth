import time

from openid.store.interface import OpenIDStore
from openid.store.nonce import SKEW


class OpenIDStore(OpenIDStore):
    """Storage class"""
    def __init__(self, strategy):
        """Init method"""
        super(OpenIDStore, self).__init__()
        self.strategy = strategy
        self.storage = strategy.storage
        self.assoc = self.storage.associations
        self.nonce = self.storage.nonce
        self.max_nonce_age = 6 * 60 * 60  # Six hours

    def storeAssociation(self, server_url, association):
        """Store new assocition if doesn't exist"""
        self.assoc.store(server_url, association)

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
