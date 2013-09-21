from social.backends.base import BaseAuth
from social.exceptions import AuthMissingParameter


class EmailAuth(BaseAuth):
    name = 'email'
    REQUIRES_EMAIL_VALIDATION = True

    def get_user_id(self, details, response):
        return details['email']

    def get_user_details(self, response):
        """Return user details, BrowserID only provides Email."""
        email = response['email']
        fullname = response.get('fullname', '')
        first_name = response.get('first_name', '')
        last_name = response.get('last_name', '')
        if fullname and not (first_name or last_name):
            try:
                first_name, last_name = fullname.split(' ', 1)
            except ValueError:
                first_name = fullname
                last_name = last_name or ''
        return {
            'username': email.split('@', 1)[0],
            'email': email,
            'fullname': fullname,
            'first_name': first_name,
            'last_name': last_name
        }

    def extra_data(self, user, uid, response, details):
        """Return users extra data, pops password if preset"""
        data = dict(response)
        data.pop('password', None)
        return data

    def auth_url(self):
        return self.setting('FORM_URL')

    def auth_html(self):
        return self.strategy.render_html(tpl=self.setting('FORM_HTML'))

    def uses_redirect(self):
        return self.setting('FORM_URL') and not \
               self.setting('FORM_HTML')

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if 'email' not in self.data:
            raise AuthMissingParameter(self, 'email')
        if self.setting('REQUIRES_PASSWORD', True):
            if not self.data.get('password'):
                raise AuthMissingParameter(self, 'password')
        kwargs.update({'response': self.data, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)
