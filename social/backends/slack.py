"""
Slack OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/slack.html
    https://api.slack.com/docs/oauth
"""
from social.backends.oauth import BaseOAuth2
import re


class SlackOAuth2(BaseOAuth2):
    """Slack OAuth authentication backend"""
    name = 'slack'
    AUTHORIZATION_URL = 'https://slack.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://slack.com/api/oauth.access'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    EXTRA_DATA = [
        ('id', 'id'),
        ('name', 'name'),
        ('real_name', 'real_name')
    ]
    REDIRECT_STATE = True

    def get_user_details(self, response):
        """Return user details from Slack account"""

        # Build the username with the team $username@$team_url
        # Necessary to get unique names for all of slack
        match = re.search("//([^.]+)\.slack\.com", response["team_url"])
        username = "%s@%s" % (response.get("name"), match.group(1))

        return {'username': username,
                'email': response["profile"].get('email', ''),
                'fullname': response["profile"].get("real_name"),
                'first_name': response["profile"].get("first_name"),
                'last_name': response["profile"].get("last_name")
                }

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        # Has to be two calls, because the users.info requires a username,
        # And we want the team information
        # https://api.slack.com/methods/auth.test
        auth_test = self.get_json('https://slack.com/api/auth.test', params={
            'token': access_token
        })

        # https://api.slack.com/methods/users.info
        data = self.get_json('https://slack.com/api/users.info', params={
            'token': access_token,
            'user': auth_test.get("user_id")
        })

        # Capture the user data, if available based on the scope
        if data.get("user"):
            out = data["user"].copy()
            # inject the team data
            out["team_id"] = auth_test.get("team_id")
            out["team"] = auth_test.get("team")
            out["team_url"] = auth_test.get("url")
        else:
            out = data.copy()
            out.update(auth_test)

        return out
