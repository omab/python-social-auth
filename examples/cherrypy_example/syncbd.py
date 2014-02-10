import sys

sys.path.append('../..')

from sqlalchemy import create_engine

import cherrypy


cherrypy.config.update({
    'SOCIAL_AUTH_USER_MODEL': 'db.user.User',
})


from social.apps.cherrypy_app.models import SocialBase
from db import Base
from db.user import User



if __name__ == '__main__':
    engine = create_engine('sqlite:///test.db')
    Base.metadata.create_all(engine)
    SocialBase.metadata.create_all(engine)
