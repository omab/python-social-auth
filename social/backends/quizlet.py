"""
Quizlet OAuth2 Sign-in backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/quizlet.html
"""
from social.backends.oauth import BaseOAuth2


class QuizletOAuth2(BaseOAuth2):
    """Quizlet OAuth2"""
    name = 'quizlet'
    ID_KEY = 'user_id'
    API_URL = 'https://api.quizlet.com/2.0/'
    AUTHORIZATION_URL = 'https://quizlet.com/authorize'
    ACCESS_TOKEN_URL = 'https://api.quizlet.com/oauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ' '
    DEFAULT_SCOPE = ['read']

    def get_user_details(self, response):
        """Return user details from Quizlet account"""
        return {
            'username': response.get('user_id'),
        }
