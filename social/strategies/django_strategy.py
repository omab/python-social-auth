from django.conf import settings
from django.http import HttpResponse
from django.db.models import Model
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.template import TemplateDoesNotExist, RequestContext, loader, engines
from django.utils.encoding import force_text
from django.utils.functional import Promise
from django.utils.translation import get_language

from social.strategies.base import BaseStrategy, BaseTemplateStrategy


class DjangoTemplateStrategy(BaseTemplateStrategy):
    def render_template(self, tpl, context):
        template = loader.get_template(tpl)
        return template.render(RequestContext(self.strategy.request, context))

    def render_string(self, html, context):
        template = loader.get_template_from_string(html)
        return template.render(RequestContext(self.strategy.request, context))


class DjangoStrategy(BaseStrategy):
    DEFAULT_TEMPLATE_STRATEGY = DjangoTemplateStrategy

    def __init__(self, storage, request=None, tpl=None):
        self.request = request
        self.session = request.session if request else {}
        super(DjangoStrategy, self).__init__(storage, tpl)

    def get_setting(self, name):
        value = getattr(settings, name)
        # Force text on URL named settings that are instance of Promise
        if name.endswith('_URL') and isinstance(value, Promise):
            value = force_text(value)
        return value

    def request_data(self, merge=True):
        if not self.request:
            return {}
        if merge:
            data = self.request.GET.copy()
            data.update(self.request.POST)
        elif self.request.method == 'POST':
            data = self.request.POST
        else:
            data = self.request.GET
        return data

    def request_host(self):
        if self.request:
            return self.request.get_host()

    def request_is_secure(self):
        """Is the request using HTTPS?"""
        return self.request.is_secure()

    def request_path(self):
        """path of the current request"""
        return self.request.path

    def request_port(self):
        """Port in use for this request"""
        return self.request.META['SERVER_PORT']

    def request_get(self):
        """Request GET data"""
        return self.request.GET.copy()

    def request_post(self):
        """Request POST data"""
        return self.request.POST.copy()

    def redirect(self, url):
        return redirect(url)

    def html(self, content):
        return HttpResponse(content, content_type='text/html;charset=UTF-8')

    def render_html(self, tpl=None, html=None, context=None):
        if not tpl and not html:
            raise ValueError('Missing template or html parameters')
        context = context or {}
        try:
            template = loader.get_template(tpl)
        except TemplateDoesNotExist:
            template = engines['django'].from_string(html)
        return template.render(RequestContext(self.request, context))

    def authenticate(self, backend, *args, **kwargs):
        kwargs['strategy'] = self
        kwargs['storage'] = self.storage
        kwargs['backend'] = backend
        return authenticate(*args, **kwargs)

    def session_get(self, name, default=None):
        return self.session.get(name, default)

    def session_set(self, name, value):
        self.session[name] = value
        if hasattr(self.session, 'modified'):
            self.session.modified = True

    def session_pop(self, name):
        return self.session.pop(name, None)

    def session_setdefault(self, name, value):
        return self.session.setdefault(name, value)

    def build_absolute_uri(self, path=None):
        if self.request:
            return self.request.build_absolute_uri(path)
        else:
            return path

    def random_string(self, length=12, chars=BaseStrategy.ALLOWED_CHARS):
        try:
            from django.utils.crypto import get_random_string
        except ImportError:  # django < 1.4
            return super(DjangoStrategy, self).random_string(length, chars)
        else:
            return get_random_string(length, chars)

    def to_session_value(self, val):
        """Converts values that are instance of Model to a dictionary
        with enough information to retrieve the instance back later."""
        if isinstance(val, Model):
            val = {
                'pk': val.pk,
                'ctype': ContentType.objects.get_for_model(val).pk
            }
        return val

    def from_session_value(self, val):
        """Converts back the instance saved by self._ctype function."""
        if isinstance(val, dict) and 'pk' in val and 'ctype' in val:
            ctype = ContentType.objects.get_for_id(val['ctype'])
            ModelClass = ctype.model_class()
            val = ModelClass.objects.get(pk=val['pk'])
        return val

    def get_language(self):
        """Return current language"""
        return get_language()
