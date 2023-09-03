from app import app
from db import db_init

def create_app():
    db_init()
    return app