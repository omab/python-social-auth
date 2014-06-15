"""Flask SQLAlchemy ORM models for Social Auth"""
from mongoengine import ReferenceField

from social.utils import setting_name, module_member
from social.storage.mongoengine_orm import MongoengineUserMixin, \
                                           MongoengineAssociationMixin, \
                                           MongoengineNonceMixin, \
                                           MongoengineCodeMixin, \
                                           BaseMongoengineStorage


class FlaskStorage(BaseMongoengineStorage):
    user = None
    nonce = None
    association = None
    code = None


def init_social(app, db):
    User = module_member(app.config[setting_name('USER_MODEL')])

    class UserSocialAuth(db.Document, MongoengineUserMixin):
        """Social Auth association model"""
        user = ReferenceField(User)

        @classmethod
        def user_model(cls):
            return User

    class Nonce(db.Document, MongoengineNonceMixin):
        """One use numbers"""
        pass

    class Association(db.Document, MongoengineAssociationMixin):
        """OpenId account association"""
        pass

    class Code(db.Document, MongoengineCodeMixin):
        pass

    # Set the references in the storage class
    FlaskStorage.user = UserSocialAuth
    FlaskStorage.nonce = Nonce
    FlaskStorage.association = Association
    FlaskStorage.code = Code
