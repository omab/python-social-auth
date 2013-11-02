from sqlalchemy import Column, Integer, String

from app import Base, engine


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    email = Column(String(75), nullable=False)
    password = Column(String(128), nullable=True)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
