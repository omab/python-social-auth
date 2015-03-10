import sys

sys.path.append('../..')

import web
from web.contrib.template import render_jinja

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from social.utils import setting_name
from social.apps.webpy_app.utils import psa, backends
from social.apps.webpy_app import app as social_app

import local_settings

web.config.debug = False
web.config[setting_name('USER_MODEL')] = 'models.User'
web.config[setting_name('AUTHENTICATION_BACKENDS')] = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.google.GoogleOpenId',
    'social.backends.google.GoogleOAuth2',
    'social.backends.google.GoogleOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.yahoo.YahooOpenId',
    'social.backends.stripe.StripeOAuth2',
    'social.backends.persona.PersonaAuth',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.yahoo.YahooOAuth',
    'social.backends.angel.AngelOAuth2',
    'social.backends.behance.BehanceOAuth2',
    'social.backends.bitbucket.BitbucketOAuth',
    'social.backends.box.BoxOAuth2',
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.github.GithubOAuth2',
    'social.backends.foursquare.FoursquareOAuth2',
    'social.backends.instagram.InstagramOAuth2',
    'social.backends.live.LiveOAuth2',
    'social.backends.vk.VKOAuth2',
    'social.backends.dailymotion.DailymotionOAuth2',
    'social.backends.disqus.DisqusOAuth2',
    'social.backends.dropbox.DropboxOAuth',
    'social.backends.eveonline.EVEOnlineOAuth2',
    'social.backends.evernote.EvernoteSandboxOAuth',
    'social.backends.fitbit.FitbitOAuth',
    'social.backends.flickr.FlickrOAuth',
    'social.backends.livejournal.LiveJournalOpenId',
    'social.backends.soundcloud.SoundcloudOAuth2',
    'social.backends.thisismyjam.ThisIsMyJamOAuth1',
    'social.backends.stocktwits.StocktwitsOAuth2',
    'social.backends.tripit.TripItOAuth',
    'social.backends.clef.ClefOAuth2',
    'social.backends.twilio.TwilioAuth',
    'social.backends.xing.XingOAuth',
    'social.backends.yandex.YandexOAuth2',
    'social.backends.podio.PodioOAuth2',
    'social.backends.mineid.MineIDOAuth2',
    'social.backends.wunderlist.WunderlistOAuth2',
)
web.config[setting_name('LOGIN_REDIRECT_URL')] = '/done/'


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
    def GET(self):
        user = self.get_current_user()
        return render.done(user=user, backends=backends(user))


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
