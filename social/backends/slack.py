"""
Slack OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/slack.html
    https://api.slack.com/docs/oauth
"""
import re

from social.backends.oauth import BaseOAuth2


class SlackOAuth2(BaseOAuth2):
    """Slack OAuth authentication backend"""
    name = 'slack'
    AUTHORIZATION_URL = 'https://slack.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://slack.com/api/oauth.access'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('id', 'id'),
        ('name', 'name'),
        ('real_name', 'real_name')
    ]

    def get_user_details(self, response):
        """Return user details from Slack account"""
        # Build the username with the team $username@$team_url
        # Necessary to get unique names for all of slack
        match = re.search(r'//([^.]+)\.slack\.com', response['url'])
        username = '{0}@{1}'.format(response.get("user"), match.group(1))

        out = {'username': username}
        if 'profile' in response:
            out.update({
                'email': response['profile'].get('email'),
                'fullname': response['profile'].get('real_name'),
                'first_name': response['profile'].get('first_name'),
                'last_name': response['profile'].get('last_name')
            })
        return out

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        # Has to be two calls, because the users.info requires a username,
        # And we want the team information. Check auth.test details at:
        #   https://api.slack.com/methods/auth.test
        auth_test = self.get_json('https://slack.com/api/auth.test', params={
            'token': access_token
        })

        # https://api.slack.com/methods/users.info
        user_info = self.get_json('https://slack.com/api/users.info', params={
            'token': access_token,
            'user': auth_test.get('user_id')
        })
        if user_info.get('user'):
            # Capture the user data, if available based on the scope
            auth_test.update(user_info['user'])

        # Clean up user_id vs id
        auth_test['id'] = auth_test['user_id']
        auth_test.pop('ok', None)
        auth_test.pop('user_id', None)
        return auth_test
