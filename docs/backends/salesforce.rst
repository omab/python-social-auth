Salesforce
==========

Salesforce uses OAuth v2 for Authentication, check the `official docs`_.

- Create an app following the steps in the `Defining Connected Apps`_ docs.

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

        SOCIAL_AUTH_SALESFORCE_OAUTH2_KEY = '<App UID>'
        SOCIAL_AUTH_SALESFORCE_OAUTH2_SECRET = '<App secret>'

- Add the backend to the ``AUTHENTICATION_BACKENDS`` setting::

        AUTHENTICATION_BACKENDS = (
            ...
            'social.backends.salesforce.SalesforceOAuth2',
            ...
        )

- Then you can start using ``{% url social:begin 'salesforce-oauth2' %}`` in
  your templates


If using the sandbox mode:

- Fill these settings instead::

        SOCIAL_AUTH_SALESFORCE_OAUTH2_SANDBOX_KEY = '<App UID>'
        SOCIAL_AUTH_SALESFORCE_OAUTH2_SANDBOX_SECRET = '<App secret>'

- And this backend::

        AUTHENTICATION_BACKENDS = (
            ...
            'social.backends.salesforce.SalesforceOAuth2Sandbox',
            ...
        )

- Then you can start using ``{% url social:begin 'salesforce-oauth2-sandbox' %}``
  in your templates

.. _official docs: https://www.salesforce.com/us/developer/docs/api_rest/Content/intro_understanding_web_server_oauth_flow.htm
.. _Defining Connected Apps: https://www.salesforce.com/us/developer/docs/api_rest/Content/intro_defining_remote_access_applications.htm
