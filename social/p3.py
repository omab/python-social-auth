import six
# Python3 support, keep import hacks here

if six.PY3:
    from urllib.parse import parse_qs, urlparse, urlunparse, quote, \
                             urlsplit, urlencode, unquote, quote_plus
    from io import StringIO
else:
    try:
        from urlparse import parse_qs
    except ImportError:  # fall back for Python 2.5
        from cgi import parse_qs
    from urlparse import urlparse, urlunparse, urlsplit
    from urllib import urlencode, unquote, quote, quote_plus
    from StringIO import StringIO
