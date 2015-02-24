"""Flask SQLAlchemy ORM models for Social Auth"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from social.utils import setting_name, module_member
from social.storage.sqlalchemy_orm import SQLAlchemyUserMixin, \
                                          SQLAlchemyAssociationMixin, \
                                          SQLAlchemyNonceMixin, \
                                          SQLAlchemyCodeMixin, \
                                          BaseSQLAlchemyStorage


PSABase = declarative_base()


class _AppSession(PSABase):
    __abstract__ = True

    @classmethod
    def _set_session(cls, app_session):
        cls.app_session = app_session

    @classmethod
    def _session(cls):
        return cls.app_session


class UserSocialAuth(_AppSession, SQLAlchemyUserMixin):
    """Social Auth association model"""
    # Temporary override of constraints to avoid an error on the still-to-be
    # missing column uid.
    __table_args__ = ()

    @classmethod
    def user_model(cls):
        return cls.user.property.argument

    @classmethod
    def username_max_length(cls):
        user_model = cls.user_model()
        return user_model.__table__.columns.get('username').type.length


class Nonce(_AppSession, SQLAlchemyNonceMixin):
    """One use numbers"""
    pass


class Association(_AppSession, SQLAlchemyAssociationMixin):
    """OpenId account association"""
    pass


class Code(_AppSession, SQLAlchemyCodeMixin):
    pass


class FlaskStorage(BaseSQLAlchemyStorage):
    user = UserSocialAuth
    nonce = Nonce
    association = Association
    code = Code


def init_social(app, session):
    UID_LENGTH = app.config.get(setting_name('UID_LENGTH'), 255)
    User = module_member(app.config[setting_name('USER_MODEL')])
    _AppSession._set_session(session)
    UserSocialAuth.__table_args__ = (UniqueConstraint('provider', 'uid'),)
    UserSocialAuth.uid = Column(String(UID_LENGTH))
    UserSocialAuth.user_id = Column(Integer, ForeignKey(User.id),
                                    nullable=False, index=True)
    UserSocialAuth.user = relationship(User, backref=backref('social_auth',
                                                             lazy='dynamic'))
