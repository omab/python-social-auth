import json

from social.tests.backends.oauth import OAuth2Test


class CoinbaseOAuth2Test(OAuth2Test):
    backend_path = 'social.backends.coinbase.CoinbaseOAuth2'
    user_data_url = 'https://coinbase.com/api/v1/users'
    expected_username = 'SatoshiNakamoto'
    access_token_body = json.dumps({
        'access_token': 'foobar',
        'token_type': 'bearer'
    })
    user_data_body = json.dumps({
        'users': [
            {
                'user': {
                    'id': "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                    'name': "Satoshi Nakamoto",
                    'email': "satoshi@nakamoto.com",
                    'pin': None,
                    'time_zone': "Eastern Time (US & Canada)",
                    'native_currency': "USD",
                    'buy_level': 2,
                    'sell_level': 2,
                    'balance': {
                        'amount': "1000000",
                        'currency': "BTC"
                    },
                    'buy_limit': {
                        'amount': "50.00000000",
                        'currency': "BTC"
                    },
                    'sell_limit': {
                        'amount': "50.00000000",
                        'currency': "BTC"
                    }
                }
            }
        ]
    })

    def test_login(self):
        self.do_login()

    def test_partial_pipeline(self):
        self.do_partial_pipeline()
