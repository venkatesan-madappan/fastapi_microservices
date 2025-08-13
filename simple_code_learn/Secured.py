from fastapi import FastAPI

from pydantic import BaseModel, ConfigDict

from db_config.sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = engine.url.URL(
    "postgresql+psycopg2",
    username="venkatesan",
    password="Sriviviji@101",
    host="localhost",
    port="5432",
    database="fcms"
    )

class Signup(Base):
    
class SignupReq(BaseModel):
    id : int
    username: str
    password: str
    model_config = ConfigDict(from_attributes=True) # inform pydantic to read data from ORM Objects

app = FastAPI()

@app.get("/index/")
def index():
    return {"context":"Welcome to Secured HTTP"}

@app.post("/signup/add/")
def signup_add(req: SignupReq):


# @app.get("/approve/signup")
# def signup_approve():
