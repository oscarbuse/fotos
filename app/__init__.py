#!/opt/venv/bin/python
# -*- coding: utf-8 -*-

"""
File: BASE/website/app/__init__.py
Purpose:
  Initialize our Flask app

__author__     = "Oscar Buse"
__copyright__  = "Copyright 2024, KwaLinux"
__credits__    = ["Oscar Buse"]
__license__    = "WTFPL (https://en.wikipedia.org/wiki/WTFPL)"
__version__    = "1.0.0"
__maintainer__ = "Oscar Buse"
__email__      = "oscar@kwalinux.nl"
__status__     = "production"
"""

# ---------------------------------------------------
# Imports
# ---------------------------------------------------
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
# after existing third-party imports
from flask_login import LoginManager
from flask_migrate import Migrate

# local imports
from config import app_config

# ---------------------------------------------------
# Variables
# ---------------------------------------------------
# db variable initialization
db = SQLAlchemy()

# after the db variable initialization
login_manager = LoginManager()

# ---------------------------------------------------
# Functions
# ---------------------------------------------------
def create_app(config_name):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_object(app_config[config_name])
  app.config.from_pyfile('config.py')

  Bootstrap5(app)

  db.init_app(app)

  login_manager.init_app(app)
  login_manager.login_message = "You must be logged in to access this page."
  login_manager.login_view = "auth.login"

  migrate = Migrate(app, db, compare_type=True)
  from app import models

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  from .home import home as home_blueprint
  app.register_blueprint(home_blueprint)

  return app
