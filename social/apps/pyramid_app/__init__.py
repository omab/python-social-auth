def includeme(config):
    config.add_route('social.auth', '/login/{backend}')
    config.add_route('social.complete', '/complete/{backend}')
    config.add_route('social.disconnect', '/disconnect/{backend}')
    config.add_route('social.disconnect_association',
                     '/disconnect/{backend}/{association_id}')
