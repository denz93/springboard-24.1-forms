from db import session
from model import Pet
from copy import copy 

class Error:
    code = None
    message = 'general error'

    def __repr__(self) -> str:
        return self.message
    
class PetNotFoundError(Error):
    message = 'Pet not found'

def get_pets(filter={}, limit=20, skip=0):
    pets = []
    pets = session.query(Pet).filter_by(**filter).limit(limit).offset(skip).all()
    return pets

def create_pet(pet_like: Pet):
    pet = copy(pet_like)
    session.add(pet)
    session.commit()
    return pet

def update_pet_by_id(id, pet_like: dict[str, any]):
    pet = session.get(Pet, id)

    if pet is None:
        raise PetNotFoundError()
    
    for key, value in pet_like.items():
        if hasattr(pet, key):
            setattr(pet, key, value)
    session.commit()
    return pet

def get_pet_by_id(id):
    return session.get(Pet, id)