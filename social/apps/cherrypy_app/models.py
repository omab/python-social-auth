"""Flask SQLAlchemy ORM models for Social Auth"""
import cherrypy

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

from social.utils import setting_name, module_member
from social.storage.sqlalchemy_orm import SQLAlchemyUserMixin, \
                                          SQLAlchemyAssociationMixin, \
                                          SQLAlchemyNonceMixin, \
                                          BaseSQLAlchemyStorage
from social.apps.flask_app.fields import JSONType


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
    __tablename__ = 'social_auth_usersocialauth'
    __table_args__ = (UniqueConstraint('provider', 'uid'),)
    id = Column(Integer, primary_key=True)
    provider = Column(String(32))
    uid = Column(String(UID_LENGTH))
    extra_data = Column(JSONType)
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
    __tablename__ = 'social_auth_nonce'
    __table_args__ = (UniqueConstraint('server_url', 'timestamp', 'salt'),)
    id = Column(Integer, primary_key=True)
    server_url = Column(String(255))
    timestamp = Column(Integer)
    salt = Column(String(40))


class Association(CherryPySocialBase, SQLAlchemyAssociationMixin, SocialBase):
    """OpenId account association"""
    __tablename__ = 'social_auth_association'
    __table_args__ = (UniqueConstraint('server_url', 'handle'),)
    id = Column(Integer, primary_key=True)
    server_url = Column(String(255))
    handle = Column(String(255))
    secret = Column(String(255))  # base64 encoded
    issued = Column(Integer)
    lifetime = Column(Integer)
    assoc_type = Column(String(64))


class CherryPyStorage(BaseSQLAlchemyStorage):
    user = UserSocialAuth
    nonce = Nonce
    association = Association
