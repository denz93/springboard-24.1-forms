from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import get_config
from model import Base, Pet
import wrapt

class SessionProxy(wrapt.ObjectProxy):
    def __init__(self):
        super().__init__(Session) 

    def _self__bind__(self, session: Session):
        self.__wrapped__ = session
    
    def __getattr__(self, name):
        return self.__wrapped__.__getattribute__(name)
    
session:Session = SessionProxy() 

def db_init():
    config = get_config()
    global session
    engine = create_engine(
        url=config.DATABASE_URI,
        echo=config.SQLALCHEMY_ECHO
    )
    session._self__bind__(Session(engine))
    Base.metadata.create_all(engine)

    