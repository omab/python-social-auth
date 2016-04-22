"""
Twilio auth backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/twilio.html
"""
from re import sub

from social.p3 import urlencode
from social.backends.base import BaseAuth


class TwilioAuth(BaseAuth):
    name = 'twilio'
    ID_KEY = 'AccountSid'

    def get_user_details(self, response):
        """Return twilio details, Twilio only provides AccountSID as
        parameters."""
        # /complete/twilio/?AccountSid=ACc65ea16c9ebd4d4684edf814995b27e
        return {'username': response['AccountSid'],
                'email': '',
                'fullname': '',
                'first_name': '',
                'last_name': ''}

    def auth_url(self):
        """Return authorization redirect url."""
        key, secret = self.get_key_and_secret()
        callback = self.strategy.absolute_uri(self.redirect_uri)
        callback = sub(r'^https', 'http', callback)
        query = urlencode({'cb': callback})
        return 'https://www.twilio.com/authorize/{0}?{1}'.format(key, query)

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        account_sid = self.data.get('AccountSid')
        if not account_sid:
            raise ValueError(self.strategy.ugettext('No AccountSid returned'))
        kwargs.update({'response': self.data, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)
