from wtforms import Form, StringField, BooleanField, IntegerField, TextAreaField, FileField
from wtforms.utils import unset_value
from wtforms.widgets import TextArea
from wtforms.validators import input_required, length, number_range, optional, url, any_of
from flask import request
from time import time
from form_validator import EitherExistWith, FileSizeLimit
import inspect 
from typing import TypeVar

T = TypeVar("T")

class FlaskFileField(FileField):
    def save(self):
        file = request.files.get(self.name)
        file.save(self.data)

    def process_data(self, value):
        self.data = None
        if self.name not in request.files:
            return None
        file = request.files.get(self.name)
        if not file.mimetype.startswith('image'):
            return None
        now = round(time())
        file_path = f'static/upload/{now}.{file.mimetype.split("/")[1]}'
        self.data = f'{file_path}'
        return self.data


class PetForm(Form):
    name = StringField(
        label='Name',
        name='name',
        description='Your pet\'s name',
        validators=[input_required(), length(max=100)])
    species = StringField(
        label='Species', 
        name='species',
        validators=[
            input_required(), 
            any_of(['dog', 'cat', 'porcupine'])
            ])
    available = BooleanField(
        label='Available',
        name='available', 
        )
    photo_url = StringField(
        label='Photo\'s URL',
        name='photo_url', validators=[url(), optional(), length(max=1000), EitherExistWith('photo_upload')]) 
    photo_upload = FlaskFileField(
        label='Photo Upload',
        validators=[FileSizeLimit(5), optional()]
    )
    age = IntegerField(
        label='Age',
        name='age', validators=[optional(), number_range(0, 30)])
    notes = TextAreaField(
        label='Notes',
        name='notes', validators=[optional(), length(max=1000)] )
    
    def create_model_instance(self, model_cls: T) -> T:
        instance = model_cls()
        model_attrs = inspect.get_annotations(model_cls)
        form_attrs = self._fields

        for attr_name in form_attrs:
            if attr_name not in model_attrs:
                continue
            setattr(instance, attr_name, getattr(self, attr_name).data)
        return instance


