from social.strategies.utils import set_current_strategy_getter
from social.apps.flask_app.utils import load_strategy


set_current_strategy_getter(load_strategy)
