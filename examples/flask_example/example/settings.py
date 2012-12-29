from example import app


app.debug = True

SECRET_KEY = 'random-secret-key'
SESSION_COOKIE_NAME = 'psa_session'
DEBUG = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
DEBUG_TB_INTERCEPT_REDIRECTS = False
SESSION_PROTECTION = 'strong'
