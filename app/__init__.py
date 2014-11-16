from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()
app = Flask(__name__)

from config.base import BaseConfig
app.config.from_object(BaseConfig)

#db = SQLAlchemy(app)
#from app import db
#db.init_db()
login_manager.init_app(app)

GLOBAL_ENDPOINTS = []

from resource_mapping import register_routes
register_routes()

for rule in GLOBAL_ENDPOINTS:
    app.add_url_rule(
        rule[0],
        view_func=rule[1]
    )
