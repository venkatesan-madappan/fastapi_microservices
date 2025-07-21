from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID, uuid1
from bcrypt import hashpw, gensalt, checkpw

app = FastAPI()

valid_users = dict()
pending_users = dict()


class User(BaseModel):
    username: str
    password: str

class ValidUser(BaseModel):
    id: UUID
    username: str
    password: str
    passphrase: str

#first sample API
@app.get("/level1/index")
def index():
    return {"message":"Welcome to FastAPI Nerds"}

@app.post("/level1/login/signup")
def signup(uname:str, passwd:str):
    if(uname == None and passwd == None):
        return ({"message": "Invalid User"})
    elif not valid_users.get(uname) == None:
        return ({"message": "User Already exists"})
    else:
        user = User(username=uname, password=passwd)
        pending_users[uname] = user
        return user

@app.post("/level1/list/users/pending")
def list_pending_users():
    return pending_users

@app.delete("/level1/delete/users/pending")
def delete_pending_users(accounts: list[str] = []):
    for user in accounts:
        del pending_users[user]
    return {"message": "Deleted pending users"}

@app.post("/level1/login/validate", response_model=ValidUser)
def approve_user(user: User):
    if not valid_users.get(user.username) == None:
        return ValidUser(id=None, username= None, password=None, passphrase=None)
    else:
        valid_user = ValidUser(id=uuid1(), username=user.username, password = user.password, passphrase=hashpw(user.password.encode(),gensalt()))
        valid_users[user.username] = valid_user
        del pending_users[user.username]
        return valid_user

@app.get("/leavel/list/users/valid")
def list_valid_users():
    return valid_users

@app.get("/level1/login")
def login(username:str, password:str):
    if valid_users.get(username) == None:
        return {"message": "Not a Valid User"}
    else:
        user = valid_users.get(username)
        if checkpw(password.encode(), user.passphrase.encode()):
           return user
        else:
            return {"message": " Invalid User"}
