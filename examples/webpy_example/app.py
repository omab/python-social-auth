import sys

sys.path.append('../..')

import web
from web.contrib.template import render_jinja

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from social.utils import setting_name
from social.apps.webpy_app.utils import strategy


web.config.debug = False
web.config[setting_name('USER_MODEL')] = 'models.User'
web.config[setting_name('AUTHENTICATION_BACKENDS')] = (
    'social.backends.google.GoogleOAuth2',
)
web.config[setting_name('LOGIN_REDIRECT_URL')] = '/done/'
web.config[setting_name('GOOGLE_OAUTH2_KEY')] = '475232891386-9tbuets6eejq7k' \
                                                '4isl4ef2dihn9afch8.apps.goo' \
                                                'gleusercontent.com'
web.config[setting_name('GOOGLE_OAUTH2_SECRET')] = 'mjbJ-9ld2Xmuaaj31Tk6BcRJ'


from social.apps.webpy_app import app as social_app


urls = (
  '^/$', 'main',
  '^/done/$', 'done',
  '', social_app.app_social
)


render = render_jinja('templates/')


class main(object):
    def GET(self):
        return render.home()


class done(social_app.BaseViewClass):
    @strategy()
    def GET(self):
        return render.done(user=self.get_current_user())


engine = create_engine('sqlite:///test.db', echo=True)


def load_sqla(handler):
    web.ctx.orm = scoped_session(sessionmaker(bind=engine))
    try:
        return handler()
    except web.HTTPError:
        web.ctx.orm.commit()
        raise
    except:
        web.ctx.orm.rollback()
        raise
    finally:
        web.ctx.orm.commit()
        # web.ctx.orm.expunge_all()


Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

app = web.application(urls, locals())
app.add_processor(load_sqla)
session = web.session.Session(app, web.session.DiskStore('sessions'))

web.db_session = Session()
web.web_session = session


if __name__ == "__main__":
    app.run()
