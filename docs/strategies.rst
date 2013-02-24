Strategies
==========

Different strategies are defined to encapsulate the different frameworks
capabilities under a common API to reuse as much code as possible.


Description
-----------

An strategy responsibility is to provide access to:

    * Request data and host information and URI building
    * Session access
    * Project settings
    * Response types (HTML and redirects)
    * HTML rendering

Different frameworks implement these features on different ways, thus the need
for these interfaces.


Implementing a new Strategy
---------------------------

The following methods must be defined on strategies sub-classes.

Request::

    def request_data(self):
        """Return current request data (POST or GET)"""
        raise NotImplementedError('Implement in subclass')

    def request_host(self):
        """Return current host value"""
        raise NotImplementedError('Implement in subclass')

    def build_absolute_uri(self, path=None):
        """Build absolute URI with given (optional) path"""
        raise NotImplementedError('Implement in subclass')


Session::

    def session_get(self, name):
        """Return session value for given key"""
        raise NotImplementedError('Implement in subclass')

    def session_set(self, name, value):
        """Set session value for given key"""
        raise NotImplementedError('Implement in subclass')

    def session_pop(self, name):
        """Pop session value for given key"""
        raise NotImplementedError('Implement in subclass')


Settings::

    def get_setting(self, name):
        """Return value for given setting name"""
        raise NotImplementedError('Implement in subclass')


Responses::

    def html(self, content):
        """Return HTTP response with given content"""
        raise NotImplementedError('Implement in subclass')

    def redirect(self, url):
        """Return a response redirect to the given URL"""
        raise NotImplementedError('Implement in subclass')

    def render_html(self, tpl=None, html=None, context=None):
        """Render given template or raw html with given context"""
        raise NotImplementedError('Implement in subclass')
