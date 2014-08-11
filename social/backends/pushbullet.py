from social.backends.oauth import BaseOAuth2
import base64

class PushbulletOAuth2(BaseOAuth2):
    """pushbullet OAuth authentication backend"""
    name = 'pushbullet'
    EXTRA_DATA = [('id', 'id')]
    ID_KEY = 'username'
    AUTHORIZATION_URL = 'https://www.pushbullet.com/authorize'
    REQUEST_TOKEN_URL = 'https://api.pushbullet.com/oauth2/token'
    ACCESS_TOKEN_URL = 'https://api.pushbullet.com/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    STATE_PARAMETER = False
    RESPONSE_TYPE = "code"

    def get_user_details(self, response):
        return {'username': response.get('access_token')}
    
    def get_user_id(self, details, response):
    	#return details.get(details['iden']);
        return self.get_json('https://api.pushbullet.com/v2/users/me',
                            params={}, headers={'Authorization': "Basic "+base64.b64encode(details['username'])})['iden']
        
        
    # def user_data(self, access_token, *args, **kwargs):
    #     """Return user data provided"""
    #     return self.get_json('https://api.pushbullet.com/v2/users/me',
    #                         params={}, headers={'Authorization': "Basic "+base64.b64encode(access_token)})

        #'access_token': access_token
		#a.eyJ0b2tlbiI6ICJ1akRvanRGSUUwV3Rqelp1SzlKbUhBIiwgInIiOiAicVVHUXBxRUdjMU9Pa2E0M3YyZEpRUjNQVXhpNWZDNFEiLCAidCI6ICJncmFudF92MyJ9.w_1dpcSUVzto1UByzY0901p0d7KSKv5_i1ESmmeH6ww