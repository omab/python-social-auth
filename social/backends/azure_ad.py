"""
Azure Active Directory/Office365 authentication backend

The flow here is a little different from regular OAuth2 flow,
because the id_token returned by Microsoft already contains
basic information (user first name, last name, and username
which is an email address) and we only need to decode it,
so no further request for details from server is made.
"""
import jwt

from social.backends.oauth import BaseOAuth2


class AzureADAuth(BaseOAuth2):
    name = 'azure_ad'
    AUTHORIZATION_URL = 'https://login.microsoftonline.com/common/oauth2/authorize'
    ACCESS_TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/token'
    REDIRECT_STATE = False

    # ID_KEY should name a unique ID for the user. Microsoft documentation for
    # the data we use (id_token claims) says:
    # oid -- Object identifier (ID) of the user object in Azure AD.
    # sub -- Token subject identifier. This is a persistent and immutable identifier
    #        for the user that the token describes. Use this value in caching logic.
    # We picked oid.
    ID_KEY = 'oid'

    def auth_complete_params(self, state=None):
        # Specify a harmless resource
        params = super(AzureADAuth, self).auth_complete_params(state)
        # The resource name of your app is supposed to work here, but we found it didn't.
        params['resource'] ='https://api.office.com/discovery/'
        return params

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data"""
        # As noted above, most backends issue an API request here, but we
        # can get the basic data by just decoding the id_token we already have.
        response = kwargs.get('response', {})
        id_token = response.get('id_token')
        if id_token:
            try:
                claims = jwt.decode(id_token, verify=False)
                return claims
            except jwt.DecodeError:
                # Token was not really jwt claims                
                pass
            except:
                import traceback; traceback.print_exc()
                raise
        return {}

    def get_user_details(self, response):
        """Return user details from AzureAD id_token claims"""
        fullname, first_name, last_name = self.get_user_names(
            first_name=response.get('given_name'),
            last_name=response.get('family_name'),
            fullname=response.get('name')
        )
        email = response['unique_name']
        return {'username': email,
                'email': email,
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

