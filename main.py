from fastapi import FastAPI
from pydantic import BaseModel
from database import session,engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine):

def get_db():
    db = session()
    try :
        yield db
    finally :
        db.close()



