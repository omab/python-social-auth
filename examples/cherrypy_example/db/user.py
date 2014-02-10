from sqlalchemy import Column, Integer, String, Boolean

from db import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    password = Column(String(200), default='')
    name = Column(String(100))
    email = Column(String(200))
    active = Column(Boolean, default=True)

    def is_active(self):
        return self.active
