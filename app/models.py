"""
File: BASE/website/app/models.py
Purpose:
  Our database model

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
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

# ---------------------------------------------------
# Classes
# ---------------------------------------------------
class User(UserMixin, db.Model):
    """
    Create a User table
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Foto(db.Model):
    """
    Create a Foto table
    """

    __tablename__ = 'fotos'

    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(200))  # basename of the the image
    title = db.Column(db.String(200))
    main_category = db.Column(db.String(40))
    exif_data = db.Column(db.Text)
    comment = db.Column(db.Text)

class Category(db.Model):
    """
    Create a Category table. Fotos can have multiple categories.
    """

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(40))
    foto_id = db.Column(db.Integer, db.ForeignKey('fotos.id'))

#class Tag(db.Model)
#   """
#    Create a Tag table
#    """
#
#    __tablename__ = 'tags'
#
#    id = db.Column(db.Integer, primary_key=True)
#    tag = db.Column(db.string(40))
#    foto_id = db.Column(db.Integer, db.ForeignKey('fotos.id'))
