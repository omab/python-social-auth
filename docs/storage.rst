Storage
=======

Different frameworks support different ORMs, Storage solves the different
interfaces moving the common API to mixins classes. These mixins are used on
apps when defining the different models used by ``python-social-auth``.


Social User
-----------

This model associates a social account data with a user in the system, it
contains the provider name and user ID (``uid``) which should identify the
social account in the remote provider, plus some extra data (``extra_data``)
which is JSON encoded field with extra information from the provider (usually
avatars and similar).

When implementing this model, it must inherits from UserMixin_ and extend the
needed methods:

* Username::

    @classmethod
    def get_username(cls, user):
        """Return the username for given user"""
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def username_max_length(cls):
        """Return the max length for username"""
        raise NotImplementedError('Implement in subclass')

* User model::

    @classmethod
    def user_model(cls):
        """Return the user model"""
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def changed(cls, user):
        """The given user instance is ready to be saved"""
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def user_exists(cls, username):
        """
        Return True/False if a User instance exists with the given arguments.
        Arguments are directly passed to filter() manager method.
        """
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def create_user(cls, username, email=None):
        """Create a user with given username and (optional) email"""
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_user(cls, pk):
        """Return user instance for given id"""
        raise NotImplementedError('Implement in subclass')

* Social user::

    @classmethod
    def get_social_auth(cls, provider, uid):
        """Return UserSocialAuth for given provider and uid"""
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get_social_auth_for_user(cls, user):
        """Return all the UserSocialAuth instances for given user"""
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def create_social_auth(cls, user, uid, provider):
        """Create a UserSocialAuth instance for given user"""
        raise NotImplementedError('Implement in subclass')

* Social disconnection::

    @classmethod
    def allowed_to_disconnect(cls, user, backend_name, association_id=None):
        """Return if it's safe to disconnect the social account for the
        given user"""
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def disconnect(cls, name, user, association_id=None):
        """Disconnect the social account for the given user"""
        raise NotImplementedError('Implement in subclass')


Nonce
-----

This is a helper class for OpenId mechanism, it stores a one-use number,
shouldn't be used by the project since it's for internal use only.

When implementing this model, it must inherits from NonceMixin_, and override
the needed method::

    @classmethod
    def use(cls, server_url, timestamp, salt):
        """Create a Nonce instance"""
        raise NotImplementedError('Implement in subclass')


Association
-----------

Another OpenId helper class, it stores basic data to keep the OpenId
association. Like Nonce_ this is for internal use only.

When implementing this model, it must inherits from AssociationMixin_, and
override the needed methods::

    @classmethod
    def store(cls, server_url, association):
        """Create an Association instance"""
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def get(cls, *args, **kwargs):
        """Get an Association instance"""
        raise NotImplementedError('Implement in subclass')

    @classmethod
    def remove(cls, ids_to_delete):
        """Remove an Association instance"""
        raise NotImplementedError('Implement in subclass')


Validation code
---------------

This class is used to keep track of email validations codes following the usual
email validation mechanism of sending an email to the user with a unique code.
This model is used by the partial pipeline ``social.pipeline.mail.mail_validation``.
Check the docs at *Email validation* in `pipeline docs`_.

When implementing the model for your framework only one method needs to be
overridden::

    @classmethod
    def get_code(cls, code):
        """Return the Code instance with the given code value"""
        raise NotImplementedError('Implement in subclass')


Storage interface
-----------------

There's a helper class used by strategies to hide the real models names under
a common API, an instance of this class is used by strategies to access the
storage modules.

When implementing this class it must inherits from BaseStorage_, add the needed
models references and implement the needed method::

    class StorageImlpementation(BaseStorage):
        user = UserModel
        nonce = NonceModel
        association = AssociationModel
        code = CodeModel

        @classmethod
        def is_integrity_error(cls, exception):
            """Check if given exception flags an integrity error in the DB"""
            raise NotImplementedError('Implement in subclass')


Sqlalchemy and Django mixins
----------------------------

Currently there are partial implementations of mixins for `Sqlalchemy ORM`_ and
`Django ORM`_ with common code used later on current implemented applications.


Models Examples
---------------

Check for current implementations for `Django App`_, `Flask App`_, `Pyramid
App`_, and `Webpy App`_ for examples of implementations.


.. _UserMixin: https://github.com/omab/python-social-auth/blob/master/social/storage/base.py#L15
.. _NonceMixin: https://github.com/omab/python-social-auth/blob/master/social/storage/base.py#L149
.. _AssociationMixin: https://github.com/omab/python-social-auth/blob/master/social/storage/base.py#L161
.. _BaseStorage: https://github.com/omab/python-social-auth/blob/master/social/storage/base.py#L201
.. _Sqlalchemy ORM: https://github.com/omab/python-social-auth/blob/master/social/storage/sqlalchemy_orm.py
.. _Django ORM: https://github.com/omab/python-social-auth/blob/master/social/storage/django_orm.py
.. _Django App: https://github.com/omab/python-social-auth/blob/master/social/apps/django_app/default/models.py
.. _Flask App: https://github.com/omab/python-social-auth/blob/master/social/apps/flask_app/models.py
.. _Pyramid App: https://github.com/omab/python-social-auth/blob/master/social/apps/pyramid_app/models.py
.. _Webpy App: https://github.com/omab/python-social-auth/blob/master/social/apps/webpy_app/models.py
.. _pipeline docs: pipeline.html#email-validation
