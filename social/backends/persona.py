"""
Mozilla Persona authentication backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/persona.html
"""
from social.utils import handle_http_errors
from social.backends.base import BaseAuth
from social.exceptions import AuthFailed, AuthMissingParameter


class PersonaAuth(BaseAuth):
    """BrowserID authentication backend"""
    name = 'persona'

    def get_user_id(self, details, response):
        """Use BrowserID email as ID"""
        return details['email']

    def get_user_details(self, response):
        """Return user details, BrowserID only provides Email."""
        # {'status': 'okay',
        #  'audience': 'localhost:8000',
        #  'expires': 1328983575529,
        #  'email': 'name@server.com',
        #  'issuer': 'browserid.org'}
        email = response['email']
        return {'username': email.split('@', 1)[0],
                'email': email,
                'fullname': '',
                'first_name': '',
                'last_name': ''}

    def extra_data(self, user, uid, response, details=None, *args, **kwargs):
        """Return users extra data"""
        return {'audience': response['audience'],
                'issuer': response['issuer']}

    @handle_http_errors
    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if 'assertion' not in self.data:
            raise AuthMissingParameter(self, 'assertion')

        response = self.get_json('https://browserid.org/verify', data={
            'assertion': self.data['assertion'],
            'audience': self.strategy.request_host()
        }, method='POST')
        if response.get('status') == 'failure':
            raise AuthFailed(self)
        kwargs.update({'response': response, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)
