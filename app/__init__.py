"""
Flask app starts from here
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

login_manager = LoginManager()
app = Flask(__name__)
Bootstrap(app)

from config.base import BaseConfig
app.config.from_object(BaseConfig)

# FIXME Turning on debug for debugging heroku
app.debug = True

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
