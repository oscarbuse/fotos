# app/home/views.py

from flask import render_template, abort
from flask_login import login_required

from . import home

from .. import db
from ..models import Foto, Category

@home.route('/', methods=['GET'])
def myhome():
    """
    Render the homepage template on the / route
    """
    fotos = (
      Foto
        .query
        .join(Category, Category.foto_id == Foto.id)
        .where(Category.category == "Grappig")
        .all()
    )
    return render_template('home/fotos.html', fotos=fotos, category="Home")

@home.route('/web/show/<subject>', methods=['GET'])
def list_fotos(subject):
    """
    Render the homepage template on the / route
    """
    print(f"Subject: {subject}")
    if subject == "Alles":
      subject = "Alle foto's"
      try:
        fotos = (
          Foto
            .query
            .all()
        )
      except Exception as e:
        print(str(e))
        abort(403)
    else:
      try:
        fotos = (
          Foto
            .query
            .join(Category, Category.foto_id == Foto.id)
            .where(Category.category == subject)
            .all()
        )
      except Exception as e:
        print(str(e))
        abort(403)

    #print(f"fotos: {fotos}")
    return render_template('home/fotos.html', fotos=fotos, category=subject)
