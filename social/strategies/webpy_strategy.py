import web

from social.strategies.base import BaseStrategy, BaseTemplateStrategy


class WebpyTemplateStrategy(BaseTemplateStrategy):
    def render_template(self, tpl, context):
        return web.template.render(tpl)(**context)

    def render_string(self, html, context):
        return web.template.Template(html)(**context)


class WebpyStrategy(BaseStrategy):
    DEFAULT_TEMPLATE_STRATEGY = WebpyTemplateStrategy

    def get_setting(self, name):
        return getattr(web.config, name)

    def request_data(self, merge=True):
        if merge:
            data = web.input(_method='both')
        elif web.ctx.method == 'POST':
            data = web.input(_method='post')
        else:
            data = web.input(_method='get')
        return data

    def request_host(self):
        return web.ctx.host

    def redirect(self, url):
        return web.seeother(url)

    def html(self, content):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        return content

    def render_html(self, tpl=None, html=None, context=None):
        if not tpl and not html:
            raise ValueError('Missing template or html parameters')
        context = context or {}
        if tpl:
            tpl = web.template.frender(tpl)
        else:
            tpl = web.template.Template(html)
        return tpl(**context)

    def session_get(self, name, default=None):
        return web.web_session.get(name, default)

    def session_set(self, name, value):
        web.web_session[name] = value

    def session_pop(self, name):
        return web.web_session.pop(name, None)

    def session_setdefault(self, name, value):
        return web.web_session.setdefault(name, value)

    def build_absolute_uri(self, path=None):
        path = path or ''
        if path.startswith('http://') or path.startswith('https://'):
            return path
        return web.ctx.protocol + '://' + web.ctx.host + path
