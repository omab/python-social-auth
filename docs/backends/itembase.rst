Itembase
=========

Itembase uses OAuth2 for authentication.

- Register a new application for the `Itembase API`_, and

- Add itembase live backend and/or sandbox backend to ``AUTHENTICATION_BACKENDS``::

      AUTHENTICATION_BACKENDS = (
        ...
        'social.backends.itembase.ItembaseOAuth2',
        'social.backends.itembase.ItembaseOAuth2Sandbox',
        ...
      )

- fill ``Client Id`` and ``Client Secret`` values in the settings::

    SOCIAL_AUTH_ITEMBASE_KEY = ''
    SOCIAL_AUTH_ITEMBASE_SECRET = ''

    SOCIAL_AUTH_ITEMBASE_SANDBOX_KEY = ''
    SOCIAL_AUTH_ITEMBASE_SANDBOX_SECRET = ''


- extra scopes can be defined by using::

    SOCIAL_AUTH_ITEMBASE_SCOPE = ['connection.transaction',
                                  'connection.product',
                                  'connection.profile',
                                  'connection.buyer']
    SOCIAL_AUTH_ITEMBASE_SANDBOX_SCOPE = SOCIAL_AUTH_ITEMBASE_SCOPE
    
To use data from the extra scopes, you need to do an extra activation step
that is not in the usual OAuth flow. For that you can extend your pipeline and
add a function that sends the user to an activation URL that Itembase provides.
The method to retrieve the activation data is included in the backend::

    @partial
    def activation(strategy, backend, response, *args, **kwargs):
        if backend.name.startswith("itembase"):
            
            if strategy.session_pop('itembase_activation_in_progress'):
                strategy.session_set('itembase_activated', True)
                
            if not strategy.session_get('itembase_activated'):
                activation_data = backend.activation_data(response)
                strategy.session_set('itembase_activation_in_progress', True)
                return HttpResponseRedirect(activation_data['activation_url'])

.. _Itembase API: http://developers.itembase.com/authentication/index
