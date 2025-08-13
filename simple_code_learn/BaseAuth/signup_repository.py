from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import Session, relationship

from db_connection import Base

class Signup(Base):
    __tablename__ = "vsignup"
    id = Column(Integer, primary_key=True, index=True)
    username = Column("username", String, unique=False, index=False)
    password = Column("password", String, unique=False, index=False)

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

class SignupRepository:
    def __init__(self, sess:Session):
        self.sess:Session = sess

    def insert_signup(self, signup:Signup) -> bool:
        try:
            self.sess.add(signup)
            self.sess.commit()
            print(signup.id)
        except:
            return False
        return True


class LoginRepository:
    def __init__(self, sess:Session):
        self.sess:Session = sess

    def get_all_login_username(self, username:str):
        return self.sess.query(Login).filter(Login.username == username).one_or_none()

class ProfileRepository: 
    def __init__(self, sess:Session):
        self.sess:Session = sess
    
    def insert_profile(self, profile: Profile) -> bool: 
        try:
            self.sess.add(profile)
            self.sess.commit()
        except: 
            return False 
        return True
    def get_profile(self, id:int): 
        return self.sess.query(Profile).filter(Profile.id == id).one_or_none()

    def get_all_profile(self):
        return self.sess.query(Profile).all() 
