"""Flask Peewee ORM models for Social Auth"""
from peewee import Model, ForeignKeyField, Proxy

from social.utils import setting_name, module_member
from social.storage.peewee_orm import PeeweeUserMixin, \
                                      PeeweeAssociationMixin, \
                                      PeeweeNonceMixin, \
                                      PeeweeCodeMixin, \
                                      BasePeeweeStorage, \
                                      database_proxy


class FlaskStorage(BasePeeweeStorage):
    user = None
    nonce = None
    association = None
    code = None


def init_social(app, db):
    User = module_member(app.config[setting_name('USER_MODEL')])

    database_proxy.initialize(db)

    class UserSocialAuth(PeeweeUserMixin):
        """Social Auth association model"""
        user = ForeignKeyField(User, related_name='social_auth')

        @classmethod
        def user_model(cls):
            return User

    class Nonce(PeeweeNonceMixin):
        """One use numbers"""
        pass

    class Association(PeeweeAssociationMixin):
        """OpenId account association"""
        pass

    class Code(PeeweeCodeMixin):
        pass

    # Set the references in the storage class
    FlaskStorage.user = UserSocialAuth
    FlaskStorage.nonce = Nonce
    FlaskStorage.association = Association
    FlaskStorage.code = Code
