"""
Shopify OAuth support.

You must:

- Register an App in the shopify partner control panel
- Add the API Key and shared secret in your django settings
- Set the Application URL in shopify app settings
- Install the shopify package

"""
import imp
from urllib2 import HTTPError

from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthFailed, AuthCanceled


class ShopifyOAuth2(BaseOAuth2):
    """Shopify OAuth2 authentication backend"""
    name = 'shopify'
    ID_KEY = 'shop'
    EXTRA_DATA = [
        ('shop', 'shop'),
        ('website', 'website'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Use the shopify store name as the username"""
        return {
            'username': unicode(response.get('shop', '')
                                        .replace('.myshopify.com', ''))
        }

    def __init__(self, request, redirect):
        super(ShopifyOAuth2, self).__init__(request, redirect)
        fp, pathname, description = imp.find_module('shopify')
        self.shopifyAPI = imp.load_module('shopify', fp, pathname, description)

    def auth_url(self):
        key, secret = self.get_key_and_secret()
        self.shopifyAPI.Session.setup(api_key=key, secret=secret)
        scope = self.get_scope()
        state = self.state_token()
        self.request.session[self.name + '_state'] = state
        redirect_uri = self.get_redirect_uri(state)
        return self.shopifyAPI.Session.create_permission_url(
            self.data.get('shop').strip(),
            scope=scope,
            redirect_uri=redirect_uri
        )

    def auth_complete(self, *args, **kwargs):
        """Completes login process, must return user instance"""
        access_token = None
        if self.data.get('error'):
            error = self.data.get('error_description') or self.data['error']
            raise AuthFailed(self, error)

        key, secret = self.get_key_and_secret()
        try:
            shop_url = self.data.get('shop')
            self.shopifyAPI.Session.setup(api_key=key, secret=secret)
            shopify_session = self.shopifyAPI.Session(shop_url, self.data)
            access_token = shopify_session.token
        except self.shopifyAPI.ValidationException, e:
            raise AuthCanceled(self)
        except HTTPError, e:
            if e.code == 400:
                raise AuthCanceled(self)
            else:
                raise
        else:
            if not access_token:
                raise AuthFailed(self, 'Authentication Failed')
        return self.do_auth(access_token, shop_url, shopify_session.url,
                            *args, **kwargs)

    def do_auth(self, access_token, shop_url, website, *args, **kwargs):
        kwargs.update({
            'backend': self,
            'response': {
                'shop': shop_url,
                'website': 'http://%s' % website,
                'access_token': access_token
            }
        })
        return self.strategy.authenticate(*args, **kwargs)


# Backend definition
BACKENDS = {
    'shopify': ShopifyOAuth2,
}
