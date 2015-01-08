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
        match = re.search("//([^.]+)\.slack\.com", response["url"])
        username = "%s@%s" % (response.get("user"), match.group(1))

        out = {'username': username}
        if response.get("profile"):
            out.update({
                'email': response["profile"].get("email"),
                'fullname': response["profile"].get("real_name"),
                'first_name': response["profile"].get("first_name"),
                'last_name': response["profile"].get("last_name")
            })
        return out

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        # Has to be two calls, because the users.info requires a username,
        # And we want the team information
        # https://api.slack.com/methods/auth.test
        auth_test = self.get_json('https://slack.com/api/auth.test', params={
            'token': access_token
        })
        out = auth_test
        del out["ok"]

        # https://api.slack.com/methods/users.info
        user_info = self.get_json('https://slack.com/api/users.info', params={
            'token': access_token,
            'user': auth_test.get("user_id")
        })

        if user_info.get("user"):
            # Capture the user data, if available based on the scope
            out.update(user_info["user"])

        # Clean up user_id vs id
        out["id"] = out["user_id"]
        del out["user_id"]

        return out
