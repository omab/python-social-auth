SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/done/'
SOCIAL_AUTH_USER_MODEL = 'models.User'
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
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
    'social.backends.evernote.EvernoteSandboxOAuth',
    'social.backends.fitbit.FitbitOAuth',
    'social.backends.flickr.FlickrOAuth',
    'social.backends.livejournal.LiveJournalOpenId',
    'social.backends.soundcloud.SoundcloudOAuth2',
    'social.backends.thisismyjam.ThisIsMyJamOAuth1',
    'social.backends.stocktwits.StocktwitsOAuth2',
    'social.backends.tripit.TripItOAuth',
    'social.backends.tripit.ClefOAuth2',
    'social.backends.twilio.TwilioAuth',
    'social.backends.xing.XingOAuth',
    'social.backends.yandex.YandexOAuth2',
    'social.backends.podio.PodioOAuth2',
    'social.backends.reddit.RedditOAuth2',
)

from local_settings import *
