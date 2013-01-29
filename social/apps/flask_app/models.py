"""Flask SQLAlchemy ORM models for Social Auth"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

from social.utils import setting_name, module_member
from social.storage.sqlalchemy_orm import SQLAlchemyUserMixin, \
                                          SQLAlchemyAssociationMixin, \
                                          SQLAlchemyNonceMixin, \
                                          BaseSQLAlchemyStorage
from social.apps.flask_app.fields import JSONType


def init_social(app, db):
    UID_LENGTH = app.config.get(setting_name('UID_LENGTH'), 255)
    User = module_member(app.config[setting_name('USER_MODEL')])

    class UserSocialAuth(db.Model, SQLAlchemyUserMixin):
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

        @classmethod
        def _session(cls):
            return cls.query.session

        @classmethod
        def _query(cls):
            return cls.query

    class Nonce(db.Model, SQLAlchemyNonceMixin):
        """One use numbers"""
        __tablename__ = 'social_auth_nonce'
        __table_args__ = (UniqueConstraint('server_url', 'timestamp', 'salt'),)
        id = Column(Integer, primary_key=True)
        server_url = Column(String(255))
        timestamp = Column(Integer)
        salt = Column(String(40))

        @classmethod
        def _session(cls):
            return cls.query.session

        @classmethod
        def _query(cls):
            return cls.query

    class Association(db.Model, SQLAlchemyAssociationMixin):
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

        @classmethod
        def _session(cls):
            return cls.query.session

        @classmethod
        def _query(cls):
            return cls.query

    class FlaskStorage(BaseSQLAlchemyStorage):
        user = UserSocialAuth
        nonce = Nonce
        association = Association

    globals().update({
        'FlaskStorage': FlaskStorage,
        'UserSocialAuth': UserSocialAuth,
        'Nonce': Nonce,
        'Association': Association
    })
    return FlaskStorage
