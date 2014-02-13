# -*- coding: utf-8 -*-
from cherrypy.process import plugins

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class SAEnginePlugin(plugins.SimplePlugin):
    def __init__(self, bus, connection_string=None):
        self.sa_engine = None
        self.connection_string = connection_string
        self.session = scoped_session(sessionmaker(autoflush=True,
                                                   autocommit=False))
        super(SAEnginePlugin, self).__init__(bus)

    def start(self):
        self.sa_engine = create_engine(self.connection_string, echo=False)
        self.bus.subscribe('bind-session', self.bind)
        self.bus.subscribe('commit-session', self.commit)

    def stop(self):
        self.bus.unsubscribe('bind-session', self.bind)
        self.bus.unsubscribe('commit-session', self.commit)
        if self.sa_engine:
            self.sa_engine.dispose()
            self.sa_engine = None

    def bind(self):
        self.session.configure(bind=self.sa_engine)
        return self.session

    def commit(self):
        try:
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.remove()
