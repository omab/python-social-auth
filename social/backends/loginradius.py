"""
LoginRadius BaseAuth/BaseOAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/loginradius.html
"""
from social.backends.oauth import BaseAuth, BaseOAuth2
from social.exceptions import AuthCanceled, AuthUnknownError
from requests import HTTPError


class LoginRadiusAuth(BaseOAuth2, BaseAuth):
    """LoginRadius BaseAuth/BaseOAuth2 authentication backend."""
    name = 'loginradius'
    ID_KEY = 'ID'
    ACCESS_TOKEN_URL = 'https://api.loginradius.com/api/v2/access_token'
    PROFILE_URL = 'https://api.loginradius.com/api/v2/userprofile'
    ACCESS_TOKEN_METHOD = 'GET'
    REDIRECT_STATE = False
    STATE_PARAMETER = False
    DEFAULT_SCOPE = None

    def uses_redirect(self):
        """Return False because we return HTML instead."""
        return self.REDIRECT_STATE

    def auth_html(self):
        """Must return login HTML content returned by provider."""
        login_script = """
        <div id="interfacecontainerdiv" class="interfacecontainerdiv"></div>
        <script src="https://hub.loginradius.com/include/js/LoginRadius.js"></script>
        <script type="text/javascript"> var options={};options.login=true;
        LoginRadius_SocialLogin.util.ready(function () { $ui = LoginRadius_SocialLogin.lr_login_settings;
        $ui.interfacesize = "";$ui.apikey =
        """
        login_script += "\"" + self.setting('KEY') + "\";"
        login_script += "$ui.callback=\"" + self.get_redirect_uri() + "\";"
        login_script += "$ui.lrinterfacecontainer =\"interfacecontainerdiv\"; " + \
                        "LoginRadius_SocialLogin.init(options);  }); </script>"
        return login_script

    def auth_headers(self):
        """Static headers."""
        return {'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'}

    def auth_complete(self, *args, **kwargs):
        """Completes logging process, must return user instance."""
        self.process_error(self.data)
        try:
            response = self.request_access_token(
                self.ACCESS_TOKEN_URL,
                params={'token': self.data.get("token"), 'secret': self.setting('SECRET')},
                data=self.auth_complete_params(self.validate_state()),
                headers=self.auth_headers(),
                method=self.ACCESS_TOKEN_METHOD
            )
        except HTTPError as err:
            if err.response.status_code == 400:
                raise AuthCanceled(self)
            else:
                raise
        except KeyError:
            raise AuthUnknownError(self)
        self.process_error(response)
        return self.do_auth(response['access_token'], response=response,
                            *args, **kwargs)

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service. Implement in subclass."""
        profile_data = self.get_json(
            self.PROFILE_URL,
            params={'access_token': access_token},
            data=self.auth_complete_params(self.validate_state()),
            headers=self.auth_headers(),
            method=self.ACCESS_TOKEN_METHOD
        )
        return profile_data

    def get_user_details(self, response):
        """Must return user details in a know internal struct:
            {'username': <username if any>,
             'email': <user email if any>,
             'fullname': <user full name if any>,
             'first_name': <user first name if any>,
             'last_name': <user last name if any>}
        """
        profile = {
            'username': response['NickName'] or '',
            'email': response['Email'][0]['Value'] or '',
            'fullname': response['FullName'] or '',
            'first_name': response['FirstName'] or '',
            'last_name': response['LastName'] or ''
        }
        return profile

    def get_user_id(self, details, response):
        """Return a unique ID for the current user, by default from server
        response.

        Since LoginRadius handles multiple providers, we need to distinguish them to prevent conflicts.
        """
        return str(response.get("Provider") + "-" + response.get(self.ID_KEY))