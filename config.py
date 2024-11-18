#!/opt/venv/bin/python
# -*- coding: utf-8 -*-

"""
File: BASE/website/config.py
Purpose:
  Defines general config (for all instances)
  
__.gitignore__ = False
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
# Classes
# ---------------------------------------------------
class Config(object):
    """
    Common configurations
    """
    # Put any configurations here that are common across all environments

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    # No systemd restart needed when modifying the templates (BASE/website/app/templates/...)
    TEMPLATES_AUTO_RELOAD = True
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False

# ---------------------------------------------------
# Variables
# ---------------------------------------------------
app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
