from flask import Flask, url_for, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_app, Pet
import os

from forms import AdoptionForm, EditPetForm

username = os.environ["PGUSER"]
password = os.environ["PGPASSWORD"]
secret_key = os.environ.get("SECRET_KEY", "default_secret_key")

app = Flask(__name__)

app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{username}:{password}@localhost:5432/adoptions"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

connect_app(app)

app.app_context().push()

@app.route('/')
def list_pets():
    """ Homepage """

    pets = Pet().query.all()

    return render_template("pet_list.html", pets = pets)

@app.route('/add', methods = ["GET","POST"])
def add_pet():

    form = AdoptionForm()

    if form.validate_on_submit():
        data = {k:v for k,v in form.data.items() if k != "csrf_token"}
        new_pet = Pet(**data)
        db.session.add(new_pet)
        db.session.commit()

        flash(f"{new_pet.name} added.")

        return redirect(url_for('list_pets'))
    else:
        # re-present form for editing
        return render_template("pet_add_form.html", form=form)
    
@app.route('/<int:pet_id>', methods = ["GET","POST"])
def edit_pet(pet_id):

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()

        flash(f"{pet.name} updated.")
        return redirect(url_for('list_pets'))
    
    else:
        # re-present form for editing
        return render_template("pet_edit_form.html", form=form, pet=pet)

