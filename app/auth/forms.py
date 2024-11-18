#!/opt/venv/bin/python
# -*- coding: utf-8 -*-

"""
File: BASE/website/app/auth/forms.py
Purpose:
  Define our forms

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
# from wsgiref.validate import validator
from flask_wtf import FlaskForm
# Registration

# We do not use Flaks login. We only import the db object.
from app import db
from wtforms import (
    StringField,
    SelectField,
    SubmitField,
    SelectMultipleField,
    TextAreaField,
    FileField,
    PasswordField,        # registration
    ValidationError       # registration
)

from wtforms.validators import (
    InputRequired,
    Email,                # registration
    EqualTo               # registration 
)
from flask_wtf.file import FileAllowed

from ..models import User # registration

# ---------------------------------------------------
# Classes (only one)
# ---------------------------------------------------
"""
Registration disabled
class RegistrationForm(FlaskForm):
    #Form for users to create new account
    email = StringField('Email', validators=[InputRequired(), Email()])
    username = StringField('Username', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[
                                        InputRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')
"""

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class FotoForm(FlaskForm):
    """
    Form for admin to add or edit a foto
    """
    cat_choices = ["Vogels", "Dieren", "Bergen","Grappig","Divers","Spiegels","Zonnig","Kamperen"]
    image_filename = FileField('Foto image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])], id='image-filename')
    title = StringField('Title', id='title')
    main_category = SelectField('Main category', choices=cat_choices)
    extra_categories = SelectMultipleField("Extra Categories", choices=cat_choices) # fotos can have multiple categories
    #exif_data = TextAreaField(validators=[InputRequired()])
    comment = TextAreaField(validators=[InputRequired()])
    submit = SubmitField('Submit')

#class CommentForm(FlaskForm)
#    """
#    Form for admin to add or edit a comment
#    """
#    comment = TextAreaField(validators=[InputRequired()])
#    submit = SubmitField('Submit')

#class TagForm(FlaskForm)
#    """
#    Form for admin to add or edit a comment
#    """
#    tag = StringField('Tag', id='tag')
#    submit = SubmitField('Submit')
