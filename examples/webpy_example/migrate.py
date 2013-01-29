from app import engine
from models import Base
from social.apps.webpy_app.models import SocialBase


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    SocialBase.metadata.create_all(engine)
