"""Flask SQLAlchemy ORM models for Social Auth"""
import web

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from social.utils import setting_name, module_member
from social.storage.sqlalchemy_orm import SQLAlchemyUserMixin, \
                                          SQLAlchemyAssociationMixin, \
                                          SQLAlchemyNonceMixin, \
                                          SQLAlchemyCodeMixin, \
                                          BaseSQLAlchemyStorage


SocialBase = declarative_base()

UID_LENGTH = web.config.get(setting_name('UID_LENGTH'), 255)
User = module_member(web.config[setting_name('USER_MODEL')])


class WebpySocialBase(object):
    @classmethod
    def _session(cls):
        return web.db_session


class UserSocialAuth(WebpySocialBase, SQLAlchemyUserMixin, SocialBase):
    """Social Auth association model"""
    uid = Column(String(UID_LENGTH))
    user_id = Column(Integer, ForeignKey(User.id),
                     nullable=False, index=True)
    user = relationship(User, backref='social_auth')

    @classmethod
    def username_max_length(cls):
        return User.__table__.columns.get('username').type.length

    @classmethod
    def user_model(cls):
        return User


class Nonce(WebpySocialBase, SQLAlchemyNonceMixin, SocialBase):
    """One use numbers"""
    pass


class Association(WebpySocialBase, SQLAlchemyAssociationMixin, SocialBase):
    """OpenId account association"""
    pass


class Code(WebpySocialBase, SQLAlchemyCodeMixin, SocialBase):
    pass


class WebpyStorage(BaseSQLAlchemyStorage):
    user = UserSocialAuth
    nonce = Nonce
    association = Association
    code = Code
