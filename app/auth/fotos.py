#!/opt/venv/bin/python # -*- coding: utf-8 -*-

"""
File: BASE/website/app/auth/fotos.py
Purpose:
  CRUD operatrions for our fotos

__author__     = "Oscar Buse"
__copyright__  = "Copyright 2023, KwaLinux"
__credits__    = ["Oscar Buse"]
__license__    = "Restricted to internal use by Solarcontrol"
__version__    = "1.0.0"
__maintainer__ = "Oscar Buse"
__email__      = "oscar@kwalinux.nl"
__status__     = "production"
"""

# ---------------------------------------------------
# Imports
# ---------------------------------------------------
from . import auth

from . forms import FotoForm
from .. import db
from ..models import Foto, Category
from flask import render_template, flash, redirect, url_for, abort, request
from flask_login import login_required
from sqlalchemy.sql import text
from werkzeug.utils import secure_filename
# for set_saved_form_data
from werkzeug.datastructures import MultiDict
from flask import session

# Get EXIF data
# Src: https://stackoverflow.com/questions/4764932/in-python-how-do-i-read-the-exif-data-for-an-image/56571871#56571871
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS, IFD

import os, re

# ---------------------------------------------------
# Functions
# ---------------------------------------------------
def get_exifdata(img):
  """
  We want to show the following exif data (we put it in string):

  Model: Canon PowerShot SX60 HS  # Model
  Datum: 2024:09:17 17:36:22      # DateTimeOriginal
  Width: 4608px                   # ExifImageWidth
  Height: 3456px                  # ExifImageHeight
  Fnumber: 6.5                    # FNumber
  Real Aperture: 5.40625          # ApertureValue
  Shutter speed: 7.96875          # ShutterSpeedValue
  Exposure time: 0.004            # ExposureTime
  ISO: 125                        # ISOSpeedRatings

  """
  # We store the data
  tags_we_want = ['Model','DateTimeOriginal','ExifImageWidth','ExifImageHeight','FNumber','ApertureValue','ShutterSpeedValue','ExposureTime','ISOSpeedRatings']
  tag_rename_hr = {
    'Model': 'Model',
    'DateTimeOriginal': 'Datum',
    'ExifImageWidth': 'Width',
    'ExifImageHeight': 'Height',
    'FNumber': 'FNumber',
    'ApertureValue': 'Real Aperture',
    'ShutterSpeedValue': 'Shutter speed',
    'ExposureTime': 'Exposure time',
    'ISOSpeedRatings': 'ISO'
  }
  exif_data = ""
  img_exif = img.getexif()
  if img_exif is None:
    print("no exif data")
    return "Geen Exif data beschikbaar"

  for k, v in img_exif.items():
    tag = TAGS.get(k, k)
    if f"{tag}" in tags_we_want:
      print(f"Base: {tag}, {v}")
      exif_data = exif_data + f"<br>{tag_rename_hr[tag]}: {str(v).strip()}"

  for ifd_id in IFD:
    try:
      ifd = img_exif.get_ifd(ifd_id)
      if ifd_id == IFD.GPSInfo:
          resolve = GPSTAGS
      else:
          resolve = TAGS

      for k, v in ifd.items():
          tag = resolve.get(k, k)
          if f"{tag}" in tags_we_want:
            print(f"More: {tag}, {v}")
            exif_data = exif_data + f"<br>{tag_rename_hr[tag]}: {str(v).strip()}"
            #exif_data[f"{tag_rename_hr[tag]}"] = f"{v}"
    except KeyError:
      pass

  #print(f"Exif: {img_exif}")
  #print(f"Tags: {ExifTags.TAGS}")
  #else:
  #  for key, val in img_exif.items():
  #    if key in ExifTags.TAGS:
  #      exifdata[f"{ExifTags.TAGS[key]}"] = f"{val}"
  #      #print(f'{ExifTags.TAGS[key]}:{val}')
  #    else:
  #      exifdata_notag[f"{key}"] = f"{val}"
  #      #print(f'{key}:{val}')
  
  return exif_data

def set_saved_form_data(form):
  """
  Add the saved form data to the form
  """
  # Set form_saved data in the form
  if session.get('form_saved') is not None:
    saved = session.pop('form_saved')

    # Create a MultiDict and put the saved data in it
    formdata = MultiDict()
    for key, value in saved.items():
      formdata.add(key, str(value))

    # Fill the form with the Multidict
    form.process(formdata=formdata)

    # Show the validation errors
    form.validate()

#def striphtml(data):
#  p = re.compile(r'<.*?>')
#  return p.sub('', data)


# ---------------------------------------------------
# Routes
# ---------------------------------------------------
@auth.route('/web/auth/fotos', methods=['GET', 'POST'])
@login_required
def list_fotos():
    """
    List all fotos
    """
    fotos = (
      Foto
        .query
        .all()
    )
    return render_template('auth/fotos/fotos.html', fotos=fotos, title="Current fotos")

@auth.route('/web/auth/fotos/add', methods=['GET', 'POST'])
@login_required
def add_foto():
  """
  Add a foto to the database   
  """
  form = FotoForm()
  if form.validate_on_submit():
    # get the uploaded filename, title and comment
    image_filename = secure_filename(form.image_filename.data.filename)
    main_category = form.main_category.data
    image_path = f"/var/www/fotos/flask/website/app/static/data/{main_category}/"
    full_image_path = os.path.join(image_path,image_filename)
    print(f"req: {request.files['image_filename']}")

    # Upload image
    image_data = request.files['image_filename'].read()
    # Create [category] folder in static/data/[main_category]/img/ if it does not exist yet
    if not os.path.exists(f"{image_path}"):
      os.makedirs(f"{image_path}")
    # Save image to static/data/[main_category]/image_filename
    if not os.path.exists(full_image_path):
      #  flash(f"Nothing done: The file {full_image_path} exists!")
      #  return redirect(url_for('auth.list_fotos'))
      try:
        open(
          os.path.join(
            image_path,
            image_filename
          ),
          'wb'
        ).write(image_data)
      except Exception as e:
        print(str(e))
        abort(403)

    img = Image.open(full_image_path)
    # Get exif data
    exif_data = get_exifdata(img)

    # Create 2 extra images: with widht 300px (thumbnail) and with width 800px (initial show).
    width = 300
    full_thumbnail_path = os.path.join(image_path,f"thumb.{image_filename}")
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img_new = img.resize((width, hsize), Image.Resampling.LANCZOS)
    img_new.save(full_thumbnail_path)

    width = 800
    full_initial_show_path = os.path.join(image_path,f"__{image_filename}")
    wpercent = (width / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img_new = img.resize((width, hsize), Image.Resampling.LANCZOS)
    img_new.save(full_initial_show_path)

    foto = Foto(image_filename=image_filename, title=form.title.data, main_category=main_category, comment=form.comment.data, exif_data=exif_data)
    try:
      db.session.add(foto)
      db.session.commit()
    except Exception as e:
      print(str(e))
      abort(403)
    # get latest inserted id to use as foreign key in categories
    db.session.refresh(foto)
    last_id = foto.id

    # Add categories. First delete all categories for this foto
    sql = f"DELETE from categories where foto_id = :foto_id"
    params = {'foto_id': last_id}
    db.session.execute(text(sql),params)
    db.session.commit()
   
    # Add per category 
    categories=form.extra_categories.data
    categories.append(form.main_category.data)
    print(f"All categories: {categories}")
    # Remove duplicates
    categories = list(set(categories))
    print(f"Cleaned categories: {categories}")
    for category in categories:
      try:
        sql = f"INSERT into categories (foto_id, category) VALUES (:foto_id, :category)"
        params = {'foto_id': last_id, 'category': category}
        result = db.session.execute(text(sql), params)
      except Exception as e:
        print(str(e))
        abort(403)
    db.session.commit()
    flash('You have successfully added a new Foto.')

    return redirect(url_for('auth.list_fotos'))

  # show add form
  return render_template('auth/fotos/foto.html', action="Add", add_foto=True, form=form, title="Add Foto")

@auth.route('/web/auth/fotos/edit/<int:foto_id>', methods=['GET', 'POST'])
@login_required
def edit_foto(foto_id):
    """
    Edit a foto
    """
    foto = Foto.query.get_or_404(foto_id)
    form = FotoForm(obj=foto)
    set_saved_form_data(form)

    if form.validate_on_submit():
      # Get extra categories for this foto_id before we remove them from the form-data
      categories=form.extra_categories.data
      categories.append(form.main_category.data)

      # Save foto data in table fotos
      new_foto_data = form.data
      new_foto_data.pop('image_filename')   # not for now..
      new_foto_data.pop('extra_categories') # not part of table "fotos"
      new_foto_data.pop('submit')
      db.session.execute(
        db
          .update(Foto)
          .where(Foto.id == foto_id)
          .values(new_foto_data)
      )
      db.session.commit()

      # Edit categories. First delete all categories for this foto
      sql = f"DELETE from categories where foto_id = :foto_id"
      params = {'foto_id': foto_id}
      db.session.execute(text(sql),params)
      db.session.commit()

      # Add per category 
      # Remove duplicates (because main_category was added)
      categories = list(set(categories))
      print(f"Cleaned categories: {categories}")
      for category in categories:
        try:
          sql = f"INSERT into categories (foto_id, category) VALUES (:foto_id, :category)"
          params = {'foto_id': foto_id, 'category': category}
          result = db.session.execute(text(sql), params)
        except Exception as e:
          print(str(e))
          abort(403)
      db.session.commit()

      flash('You have successfully edited the foto.')

      # redirect to the home dashboard
      return redirect(url_for('auth.list_fotos'))
    else:
      print("NOT validated")
      for errorMessages in form.errors.items():
        for err in errorMessages:
          print(err)

    return render_template('auth/fotos/foto.html', action="Edit", add_foto=False, form=form, foto_id=foto_id, foto=foto, title="Edit foto")

@auth.route('/web/auth/fotos/delete/<int:foto_id>', methods=['GET', 'POST'])
@login_required
def delete_foto(foto_id):
    """
    Delete a foto from the database
    """
    # First delete all categories have foto_id
    categories = Category.query.filter_by(foto_id=foto_id).all()
    for category in categories:
      db.session.delete(category)
    db.session.commit()

    # Now delete the foto
    foto = Foto.query.get_or_404(foto_id)
    db.session.delete(foto)
    db.session.commit()
    flash('You have successfully deleted the foto.')

    # redirect to the fotos page
    return redirect(url_for('auth.list_fotos'))





