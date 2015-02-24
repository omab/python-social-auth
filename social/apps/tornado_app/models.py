"""Tornado SQLAlchemy ORM models for Social Auth"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from social.utils import setting_name, module_member
from social.storage.sqlalchemy_orm import SQLAlchemyUserMixin, \
                                          SQLAlchemyAssociationMixin, \
                                          SQLAlchemyNonceMixin, \
                                          SQLAlchemyCodeMixin, \
                                          BaseSQLAlchemyStorage


class TornadoStorage(BaseSQLAlchemyStorage):
    user = None
    nonce = None
    association = None
    code = None


def init_social(Base, session, settings):
    UID_LENGTH = settings.get(setting_name('UID_LENGTH'), 255)
    User = module_member(settings[setting_name('USER_MODEL')])
    app_session = session

    class _AppSession(object):
        @classmethod
        def _session(cls):
            return app_session

    class UserSocialAuth(_AppSession, Base, SQLAlchemyUserMixin):
        """Social Auth association model"""
        uid = Column(String(UID_LENGTH))
        user_id = Column(Integer, ForeignKey(User.id),
                         nullable=False, index=True)
        user = relationship(User, backref=backref('social_auth',
                                                  lazy='dynamic'))

        @classmethod
        def username_max_length(cls):
            return User.__table__.columns.get('username').type.length

        @classmethod
        def user_model(cls):
            return User

    class Nonce(_AppSession, Base, SQLAlchemyNonceMixin):
        """One use numbers"""
        pass

    class Association(_AppSession, Base, SQLAlchemyAssociationMixin):
        """OpenId account association"""
        pass

    class Code(_AppSession, Base, SQLAlchemyCodeMixin):
        pass

    # Set the references in the storage class
    TornadoStorage.user = UserSocialAuth
    TornadoStorage.nonce = Nonce
    TornadoStorage.association = Association
    TornadoStorage.code = Code
