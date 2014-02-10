from social.strategies.utils import set_current_strategy_getter
from social.apps.pyramid_app.utils import load_strategy


def includeme(config):
    config.add_route('social.auth', '/login/{backend}')
    config.add_route('social.complete', '/complete/{backend}')
    config.add_route('social.disconnect', '/disconnect/{backend}')
    config.add_route('social.disconnect_association',
                     '/disconnect/{backend}/{association_id}')


set_current_strategy_getter(load_strategy)
