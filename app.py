from flask import Flask, render_template, request, flash, get_flashed_messages
from model import Pet
from pet_form import PetForm
from pet_service import get_pets, create_pet, get_pet_by_id, update_pet_by_id
from config import get_config

app = Flask(__name__)
config = get_config()
app.secret_key = config.SECRET_KEY
@app.get('/')
def home_page():
    filter_args = dict(filter(lambda t: hasattr(Pet, t[0]), request.args.items()))
    pets = get_pets(filter=filter_args)
    return render_template('home.html', pets=pets)

@app.get('/pets/new')
def new_pet_page():
    form=PetForm()
    return render_template('new-pet.html', form=form)

@app.get('/<int:pet_id>')
def edit_pet_page(pet_id: int):
    pet = get_pet_by_id(pet_id)
    form = PetForm(obj=pet)
    form.name.render_kw = {"type":"hidden"}
    form.age.render_kw = {"type":"hidden"}
    form.species.render_kw = {"type":"hidden"}


    return render_template('edit-pet.html', form=form, pet=pet)

@app.post('/<int:pet_id>')
def edit_pet(pet_id):
    pet = get_pet_by_id(pet_id)
    
    if pet is None:
        return render_template("edit-pet.html", pet=None)
    
    form = PetForm(request.form)
    form.name.render_kw = {"type":"hidden"}
    form.age.render_kw = {"type":"hidden"}
    form.species.render_kw = {"type":"hidden"}
    print(request.form)
    if not form.validate():
        for field_name, error_messages in form.errors.items():
            flash(f"{field_name.capitalize()}: {'. '.join(error_messages)}", "error" )
        return render_template("edit-pet.html", form=form, pet=pet)
    if form.photo_upload.data:
        form.photo_upload.save()
        form.photo_url.data = "/" + form.photo_upload.data

    pet = update_pet_by_id(pet_id, {
        "available": form.available.data,
        "notes": form.notes.data,
        "photo_url": form.photo_url.data
    })

    flash(f"Update pet '{pet.name}' success", "success")
    return render_template("edit-pet.html", form=form, pet=pet)

@app.post('/pets/new')
def create_new_pet():
    form = PetForm(request.form)
    if not form.validate():
        for field_name, error_messages in form.errors.items():
            flash(f"{field_name.capitalize()}: {'. '.join(error_messages)}", "error" )
        return render_template('new-pet.html', form=form)
    if form.photo_upload.data:
        form.photo_upload.save()
        form.photo_url.data = "/" + form.photo_upload.data
    pet = form.create_model_instance(Pet)
    create_pet(pet)
    flash(f"Pet '{pet.name}' created", "success")
    return render_template('new-pet.html', form=PetForm())