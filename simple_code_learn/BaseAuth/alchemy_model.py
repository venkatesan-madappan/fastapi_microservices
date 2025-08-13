from fastapi import FastAPI

from pydantic import BaseModel, ConfigDict

from db_config.sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class SignupReq(BaseModel):
    id : int
    username: str
    password: str
    model_config = ConfigDict(from_attributes=True) # inform pydantic to read data from ORM Objects

