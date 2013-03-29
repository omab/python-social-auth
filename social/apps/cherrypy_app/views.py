from social.actions import do_auth, do_complete, do_disconnect


class CherryPyPSAViews(object):
    def auth(self, backend):
        return do_auth(self.strategy)

    def complete(self, backend, *args, **kwargs):
        # TODO: pass login and pass current user
        return do_complete(self.strategy, *args, **kwargs)

    def disconnect(self, backend, association_id=None):
        # TODO: pass current user
        return do_disconnect(self.strategy, association_id)
