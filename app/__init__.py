from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()
app = Flask(__name__)

from config.base import BaseConfig
app.config.from_object(BaseConfig)

login_manager.init_app(app)
login_manager.login_view = 'login'

GLOBAL_ENDPOINTS = []

from resource_mapping import register_routes
register_routes()

for rule in GLOBAL_ENDPOINTS:
    app.add_url_rule(
        rule[0],
        view_func=rule[1]
    )
