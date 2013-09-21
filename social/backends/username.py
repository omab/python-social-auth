from social.backends.base import BaseAuth
from social.exceptions import AuthMissingParameter


class UsernameAuth(BaseAuth):
    name = 'username'

    def get_user_id(self, details, response):
        return details['username']

    def get_user_details(self, response):
        """Return user details"""
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
            'username': response['username'],
            'email': response.get('email') or '',
            'fullname': fullname,
            'first_name': first_name,
            'last_name': last_name
        }

    def auth_url(self):
        return self.setting('FORM_URL')

    def auth_html(self):
        return self.strategy.render_html(tpl=self.setting('FORM_HTML'))

    def uses_redirect(self):
        return self.setting('FORM_URL') and not \
               self.setting('FORM_HTML')

    def auth_complete(self, *args, **kwargs):
        """Completes loging process, must return user instance"""
        if 'username' not in self.data:
            raise AuthMissingParameter(self, 'username')
        kwargs.update({'response': self.data, 'backend': self})
        return self.strategy.authenticate(*args, **kwargs)
