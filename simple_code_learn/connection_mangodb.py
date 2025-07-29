# https://www.datacamp.com/tutorial/sqlalchemy-tutorial-examples
#FastAPI Imports
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict


#SQL Alchemy Imports
from sqlalchemy import Column, String, Integer, __version__, engine, MetaData, Table, inspect
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from uuid import UUID, uuid1

print("Welcome to SQLALchemy")

url_object = engine.url.URL(
    "postgresql+psycopg2",
    username="venkatesan",
    password="Sriviviji@101",
    host="localhost",
    port="5432",
    database="fcms"
    )

print("Exploring SQLALchemy")
print(__version__)
engine = create_engine(url_object, echo=True)
sessionLocal = sessionmaker(bind=engine)

app = FastAPI()

Base = declarative_base()

# SQLAlchemy Model
class Signup(Base):
    __tablename__ = "signup"
    id = Column(Integer, primary_key=True, index=True)
    username = Column('username', String, unique=False, index=False)
    password = Column('password',String, unique=False, index=False)

# Pydantic request model
class SignupCreate(BaseModel):
    username:str
    password:str

class UserOut(BaseModel):
    id: UUID
    username:str
    model_config = ConfigDict(from_attributes=True) # inform pydantic to read data from ORM Objects

#Post Endpoint
@app.post("/signup/")
def create_signup(user: SignupCreate):
    db = sessionLocal()
    db_user = Signup(id=uuid1(), username=user.username, password=user.password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"id":db_user.id, "username":db_user.username}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, details=str(e))
    finally:
        db.close()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@app.get("/listusers", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    users = db.query(Signup).all()
    return users

Base.metadata.create_all(engine)

# inspector = inspect(engine)

# table_names = inspector.get_table_names()

# print(table_names)
