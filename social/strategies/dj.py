from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Model
from django.db.utils import IntegrityError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate
from django.template import TemplateDoesNotExist, RequestContext, loader

from social.strategies.base import BaseStrategy


class DjangoStrategy(BaseStrategy):
    def get_setting(self, name):
        return getattr(settings, name)

    def request_data(self):
        # Use request because some auth providers use POST urls with needed
        # GET parameters on it
        return self.request.REQUEST

    def request_query_string(self):
        return self.request.META.get('QUERY_STRING', '')

    def request_host(self):
        return self.request.get_host()

    def redirect(self, url):
        return HttpResponseRedirect(url)

    def html(self, content):
        return HttpResponse(content, content_type='text/html;charset=UTF-8')

    def render_html(self, tpl=None, html=None, context=None):
        if not tpl and not html:
            raise ValueError('Missing template or html parameters')
        context = context or {}
        try:
            template = loader.get_template(html)
        except TemplateDoesNotExist:
            template = loader.get_template_from_string(html)
        return template.render(RequestContext(self.request, context))

    def get_current_user(self, *args, **kwargs):
        return self.request.user

    def authenticate(self, *args, **kwargs):
        kwargs['strategy'] = self
        kwargs['storage'] = self.storage
        kwargs['backend'] = self.backend
        return authenticate(*args, **kwargs)

    def session_get(self, name, default=None):
        return self.request.session.get(name, default)

    def session_set(self, name, value):
        self.request.session[name] = value
        self.request.session.modified = True

    def session_setdefault(self, name, value):
        return self.request.session.setdefault(name, value)

    def to_session(self, next, backend, *args, **kwargs):
        """Returns dict to store on session for partial pipeline."""
        return {
            'next': next,
            'backend': backend.name,
            'args': tuple(map(self._ctype, args)),
            'kwargs': dict((key, self._ctype(val))
                                for key, val in kwargs.iteritems())
        }

    def from_session(self, session):
        """Takes session saved data to continue pipeline and merges with any
        new extra argument needed. Returns tuple with next pipeline index
        entry, arguments and keyword arguments to continue the process."""
        saved_args = map(self._model, session['args'])
        saved_kwargs = dict((key, self._model(val))
                            for key, val in session['kwargs'].iteritems())
        return session['next'], saved_args, saved_kwargs

    def build_absolute_uri(self, path=None):
        return self.request.build_absolute_uri(path)

    def clean_partial_pipeline(self):
        name = self.setting('PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        self.request.session.pop(name, None)

    def random_string(self, length=12, chars=BaseStrategy.ALLOWED_CHARS):
        try:
            from django.utils.crypto import get_random_string
        except ImportError:  # django < 1.4
            return super(DjangoStrategy, self).random_string(length, chars)
        else:
            return get_random_string(length, chars)

    def is_integrity_error(exception):
        return exception.__class__ is IntegrityError

    def _ctype(self, val):
        """Converts values that are instance of Model to a dictionary
        with enough information to retrieve the instance back later."""
        if isinstance(val, Model):
            val = {
                'pk': val.pk,
                'ctype': ContentType.objects.get_for_model(val).pk
            }
        return val

    def _model(self, val):
        """Converts back the instance saved by self._ctype function."""
        if isinstance(val, dict) and 'pk' in val and 'ctype' in val:
            ctype = ContentType.objects.get_for_id(val['ctype'])
            ModelClass = ctype.model_class()
            val = ModelClass.objects.get(pk=val['pk'])
        return val
