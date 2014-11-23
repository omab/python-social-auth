from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

from flask.ext.login import UserMixin

from flask_example import db_session


Base = declarative_base()
Base.query = db_session.query_property()


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    password = Column(String(200), default='')
    name = Column(String(100))
    email = Column(String(200))
    active = Column(Boolean, default=True)

    def is_active(self):
        return self.active
