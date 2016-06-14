"""
Flask app starts from here
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from app.db.orm import UserAbstraction
from config import Config
from resource_mapping import RULES

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
Bootstrap(app)


# FIXME Turning on debug for debugging heroku
app.debug = True

login_manager.init_app(app)
login_manager.login_view = 'login'


for rule, func in RULES:
    app.add_url_rule(rule, view_func=func)


@login_manager.user_loader
def user_load(userid):
    return UserAbstraction().get(userid)

