# -*- coding: utf-8 -*-
import cherrypy


class SATool(cherrypy.Tool):
    def __init__(self):
        super(SATool, self).__init__('before_handler', self.bind_session,
                                     priority=20)

    def _setup(self):
        super(SATool, self)._setup()
        cherrypy.request.hooks.attach('on_end_resource',
                                      self.commit_transaction,
                                      priority=80)

    def bind_session(self):
        session = cherrypy.engine.publish('bind-session').pop()
        cherrypy.request.db = session

    def commit_transaction(self):
        if not hasattr(cherrypy.request, 'db'):
            return
        cherrypy.request.db = None
        cherrypy.engine.publish('commit-session')
