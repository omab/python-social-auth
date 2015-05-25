Microsoft Azure Active Directory / Office365
============================================

Azure Active Directory uses OAuth2 for its connect workflow.

- Register a new application at `Microsoft Azure Portal`_, set your site
  domain as redirect domain,

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_AZURE_AD_KEY = ''
      SOCIAL_AUTH_AZURE_AD_SECRET = ''

- Also it's possible to define extra permissions with::

     SOCIAL_AUTH_AZURE_AD_SCOPE = [...]

  Default is empty, which is enough to retrieve the user's first name,
  last name and email.

- Make sure to have a valid ``Redirect URL`` (``http://your-domain/complete/azure_ad``)
  defined for the application in the portal.

.. _Microsoft Azure Portal: https://manage.windowsazure.com/
