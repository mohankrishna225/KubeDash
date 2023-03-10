#!/usr/bin/env python3

import os
from flask import Flask
from flask_talisman import Talisman
from sqlalchemy_utils import database_exists

from functions.components import db, login_manager, csrf
from functions.routes import main
from functions.user import UserCreate, RoleCreate
from config import app_config

csp = {
    'font-src': [
        '\'self\'',
        '*.gstatic.com'
    ],
    'style-src': [
        '\'self\'',
        'fonts.googleapis.com',
    ],
}

# Roles
roles = [
    "Admin",
    "User",
]

def db_init():
    for r in roles:
        RoleCreate(r)
    UserCreate("admin", "admin", None, "Local", "Admin")

def create_app(config_name="development"):
    app = Flask(__name__, static_url_path='', static_folder='static')

    if os.getenv('FLASK_CONFIG') == "production":
        config_name = "production"
        os.environ['LOGGING_LEVEL'] = "INFO"
    else:
        os.environ['LOGGING_LEVEL'] = "INFO"
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app.config.from_object(app_config[config_name])

    db.init_app(app)
    if not database_exists("sqlite:///"+config_name+".db"):
        with app.app_context():
            db.create_all()
            db_init()
    else:
        db_init()

    login_manager.init_app(app)
    login_manager.login_view = "main.login"
    login_manager.session_protection = "strong"

    csrf.init_app(app)

    talisman = Talisman(app, content_security_policy=csp)

    ##############################################################
    ## Custom jinja2 filter
    ##############################################################
    from functions.jinja2_decoders import j2_b64decode, j2_b64encode, split_uppercase

    app.add_template_filter(j2_b64decode)
    app.add_template_filter(j2_b64encode)
    app.add_template_filter(split_uppercase)
    
    app.register_blueprint(main)
    return app

app = create_app()

if __name__ == '__main__':
    app.run(port=8000)