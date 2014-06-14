"""Flask SQLAlchemy ORM models for Social Auth"""
import cherrypy

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from social.utils import setting_name, module_member
from social.storage.sqlalchemy_orm import SQLAlchemyUserMixin, \
                                          SQLAlchemyAssociationMixin, \
                                          SQLAlchemyNonceMixin, \
                                          BaseSQLAlchemyStorage


SocialBase = declarative_base()

DB_SESSION_ATTR = cherrypy.config.get(setting_name('DB_SESSION_ATTR'), 'db')
UID_LENGTH = cherrypy.config.get(setting_name('UID_LENGTH'), 255)
User = module_member(cherrypy.config[setting_name('USER_MODEL')])


class CherryPySocialBase(object):
    @classmethod
    def _session(cls):
        return getattr(cherrypy.request, DB_SESSION_ATTR)


class UserSocialAuth(CherryPySocialBase, SQLAlchemyUserMixin, SocialBase):
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


class Nonce(CherryPySocialBase, SQLAlchemyNonceMixin, SocialBase):
    """One use numbers"""
    pass


class Association(CherryPySocialBase, SQLAlchemyAssociationMixin, SocialBase):
    """OpenId account association"""
    pass


class CherryPyStorage(BaseSQLAlchemyStorage):
    user = UserSocialAuth
    nonce = Nonce
    association = Association
