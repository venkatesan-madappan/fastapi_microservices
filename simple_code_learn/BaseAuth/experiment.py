import os

# print("is it correct")
os.environ['MY_ENV'] = 'Environment Variable'
temp = os.getenv('MY_ENV')
print(temp)

'''
from bcrypt import hashpw, gensalt, checkpw

username = "venkatesan"
password = "venki"
passphrase = password.encode(),gensalt()
print(f" User Name : {username}")
print(f" Password : {password}")
print(f" Passphrase : {passphrase[1].decode('ascii')}")
'''

'''
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import Session, relationship

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

Base = declarative_base()

class Signup(Base):
    __tablename__ = "vsignup"
    id = Column(Integer, primary_key=True, index=True)
    username = Column("username", String, unique=False, index=False)
    pasword = Column("password", String, unique=False, index=False)

class Login(Base): 
    __tablename__ = "login"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=False, index=False)
    password = Column(String, unique=False, index=False)
    passphrase = Column(String, unique=False, index=False)
    approved_date = Column(Date, unique=False, index=False)
       
    profiles = relationship('Profile', back_populates="login", uselist=False)

class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, unique=False, index=False)
    lastname = Column(String, unique=False, index=False)
    age = Column(Integer, unique=False, index=False)
    membership_date = Column(Date, unique=False, index=False)
    member_type = Column(String, unique=False, index=False)
    login_id = Column(Integer, ForeignKey('login.id'), unique=False, index=False)
    status = Column(Integer, unique=False, index=False)

    login = relationship('Login', back_populates="profiles")


DB_URL = URL.create(
    "postgresql+psycopg2",
    username="venkatesan",
    password="Sriviviji@101",
    host="localhost",
    port="5432",
    database="fcms"
    )

db_engine = create_engine(DB_URL, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
# SessionFactory = sessionmaker(bind=db_engine)

print("Db Creation starts")
Base.metadata.create_all(bind=db_engine)
print("Db Creation Ends")
'''