"""Flask SQLAlchemy ORM models for Social Auth"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import UniqueConstraint

from social.utils import setting_name, module_member
from social.storage.sqlalchemy_orm import SQLAlchemyUserMixin, \
                                          SQLAlchemyAssociationMixin, \
                                          SQLAlchemyNonceMixin, \
                                          SQLAlchemyCodeMixin, \
                                          BaseSQLAlchemyStorage
from social.apps.flask_app.fields import JSONType


class FlaskStorage(BaseSQLAlchemyStorage):
    user = None
    nonce = None
    association = None
    code = None


def init_social(app, db):
    UID_LENGTH = app.config.get(setting_name('UID_LENGTH'), 255)
    User = module_member(app.config[setting_name('USER_MODEL')])
    app_session = db.session

    class _AppSession(object):
        @classmethod
        def _session(cls):
            return app_session

    class UserSocialAuth(_AppSession, db.Model, SQLAlchemyUserMixin):
        """Social Auth association model"""
        __tablename__ = 'social_auth_usersocialauth'
        __table_args__ = (UniqueConstraint('provider', 'uid'),)
        id = Column(Integer, primary_key=True)
        provider = Column(String(32))
        uid = Column(String(UID_LENGTH))
        extra_data = Column(JSONType)
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

    class Nonce(_AppSession, db.Model, SQLAlchemyNonceMixin):
        """One use numbers"""
        __tablename__ = 'social_auth_nonce'
        __table_args__ = (UniqueConstraint('server_url', 'timestamp', 'salt'),)
        id = Column(Integer, primary_key=True)
        server_url = Column(String(255))
        timestamp = Column(Integer)
        salt = Column(String(40))

    class Association(_AppSession, db.Model, SQLAlchemyAssociationMixin):
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

    class Code(_AppSession, db.Model, SQLAlchemyCodeMixin):
        __tablename__ = 'social_auth_code'
        __table_args__ = (UniqueConstraint('code', 'email'),)
        id = Column(Integer, primary_key=True)
        email = Column(String(200))
        code = Column(String(32), index=True)

    # Set the references in the storage class
    FlaskStorage.user = UserSocialAuth
    FlaskStorage.nonce = Nonce
    FlaskStorage.association = Association
    FlaskStorage.code = Code
