from sqlalchemy import Column, Integer, String, Boolean

from werkzeug.security import generate_password_hash, check_password_hash

from flask.ext.login import UserMixin

from example import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    password = Column(String(200), default='')
    name = Column(String(100))
    email = Column(String(200))
    active = Column(Boolean, default=True)

    def is_active(self):
        return self.active

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def valid_password(self, password):
        return check_password_hash(self.password, password)
