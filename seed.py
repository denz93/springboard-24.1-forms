import requests
from model import Pet
from random import randint
from db import db_init, session

def generate_random_data():
    SIZE = 10
    db_init()
    for i in range(0, SIZE):
        user = fetch_user()
        dog_img = fetch_dog_img()
        pet = Pet(
            name=user['first_name'], 
            photo_url=dog_img, 
            available= i < 5,
            species='dog',
            age=randint(0, 12))
        session.add(pet)
    session.commit()
        
def fetch_user():
    res = requests.get('https://random-data-api.com/api/v2/users')
    return res.json()

def fetch_dog_img():
    res = requests.get('https://random.dog/woof.json')
    data = res.json()
    return data["url"]

if __name__ == '__main__':
    generate_random_data()