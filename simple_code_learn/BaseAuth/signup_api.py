from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from Signup_model import SignupReq, ProfileReq
from signup_repository import Signup, Profile, SignupRepository, LoginRepository, ProfileRepository
from basic_security import http_basic, authenticate
from db_connection import sess_db


app = FastAPI()


@app.get("/index/")
def index():
    return {"context":"Welcome to Secured HTTP"}

@app.post("/signup/add/")
def signup_add(req: SignupReq, credentials: HTTPBasicCredentials = Depends(http_basic), sess:Session = Depends(sess_db)):
    repo:SignupRepository = SignupRepository(sess)
    signup = Signup(id = req.id, username = req.username, password = req.password)
    result = repo.insert_signup(signup)
    if result == True:
        return signup
    else:
        return JSONResponse(content={'message':'create signup encountered a problem'}, status_code=500)

@app.post("/profile/add/")
def add_profile(req:ProfileReq, credentials:HTTPBasicCredentials = Depends(http_basic), sess:Session = Depends(sess_db)):
    profile_dict = req.dict(exclude_unset=True)
    repo:ProfileRepository = ProfileRepository(sess)
    profile = Profile(**profile_dict)
    result = repo.insert_profile(profile)
    if result == True:
        return Profile
    else:
        return JSONResponse(content={'message':'create profile problem encountered'}, status_code=500)


@app.post("/login/")
def loging(credentials: HTTPBasicCredentials = Depends(http_basic), sess:Session = Depends(sess_db)):
    loginrepo = LoginRepository(sess)
    account = loginrepo.get_all_login_username(credentials.username)
    print(f" Account Details {account}")
    if authenticate(credentials, account) and not account == None:
        print("Authentication Successful")
        return None
    else:
        print("What is wrong here")
        raise HTTPException(status_code=400, detail="Incorrect Username or Password")

# @app.get("/approve/signup")
# def signup_approve():
