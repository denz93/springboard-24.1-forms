from flask import request
from wtforms.validators import ValidationError
from math import ceil
DEFAULT_MAX_SIZE = 5
MB = 1024 * 1024
def FileSizeLimit(max_size_in_mb=DEFAULT_MAX_SIZE):
    max_size = max_size_in_mb * MB
    def validator(form, field):
        file = request.files[field.name]
        file.stream.read()
        size = file.stream.tell() if field.data else 0
        file.stream.seek(0)
        if size > max_size:
            raise ValidationError(f'Field "{field.name}" whose length is {ceil(size/MB * 10) /10}MB must be less than or equal {max_size_in_mb} MB')
    return validator

def EitherExistWith(field_name):
    def validator(form, field):        
        other_field = getattr(form, field_name)
        
        if hasattr(other_field, 'data') and other_field.data and hasattr(field, 'data') and field.data:
            raise ValidationError(f'Either field "{field.name}" or field "{field_name}" should exist')
        
    return validator