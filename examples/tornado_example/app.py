import sys

sys.path.append('../..')

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

from social.apps.tornado_app.routes import SOCIAL_AUTH_ROUTES

define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/home.html")


class DoneHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/done.html")


class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.request.redirect("/")


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/done", DoneHandler),
        (r"/logout", LogoutHandler),
    ] + SOCIAL_AUTH_ROUTES)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
