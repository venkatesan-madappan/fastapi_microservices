from fastapi import FastAPI, Form, Cookie, Header, Response
from pydantic import BaseModel
from uuid import UUID, uuid1
from bcrypt import hashpw, gensalt, checkpw

from datetime import date, datetime
from enum import Enum
import random
import string

app = FastAPI()

valid_users = dict()
valid_profiles = dict()
pending_users = dict()
discussion_posts = dict()
request_headers = dict()
cookies = dict()


class User(BaseModel):
    username: str
    password: str

class ValidUser(BaseModel):
    id: UUID
    username: str
    password: str
    passphrase: str

class UserType(str, Enum):
    admin = "admin"
    teacher = "teacher"
    alumini = "alumini"
    student = "student"

class UserProfile(BaseModel):
    firstname: str
    lastname: str
    middle_initial: str
    age: int = 0
    salary: int = 0
    birthday: date
    user_type: UserType

class PostType(str, Enum):
    information = "information"
    inquiry = "inquiry"
    quote = "quote"
    twit = "twit"

class Post(BaseModel):
    topic: str = None
    message: str
    date_posted: datetime

class ForumPost(BaseModel):
    id: UUID
    topic: str = None
    message: str
    post_type: PostType
    date_posted: datetime
    username:str

class ForumDiscussion(BaseModel):
    id: UUID
    main_post: ForumPost
    replies: list[ForumPost] = None
    author: UserProfile

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

@app.delete("/level1/login/remove/all")
def delete_users(username: list[str]):
    for user in username:
        del valid_users[user]
    return {"message": "All the users deleted"}

@app.delete("/level/login/remove/{username}")
def delete_user(username: str):
    del valid_users[username]
    return {"message": " deleted the user"}

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

@app.get("level1/login/password/change")
def change_password(username: str, old_passwrd: str, new_password):
    password_len = 8
    if valid_users.get(username) == None:
        return {"message": "Unknown User"}
    elif old_passwrd == "" or new_password == "":
        characters = string.ascii_lowercase
        temporary_password = ''.join(random.choice(characters) for i in range(password_len))
        user = valid_users.get(username)
        user.password = temporary_password
        user.passphrase = hashpw(temporary_password.encode(), gensalt())
        return user
    else:
        user = valid_users.get(username)
        if user.password == old_passwrd:
            user.passowrd = new_password
            user.passphrase = hashpw(new_password.encode(), gensalt())
            return user
        else:
            return {"message": "Invalid User"}

@app.post("level1/login/username/unlock")
def unlock_username(id: UUID | None):
    if id == None:
        return {"message": "Token Needed"}
    else:
        for key, value in valid_users.items():
            if value.id == id:
                return {"username": value.username}
        return {"message": " User does not exist"}

@app.post("level1/login/password/unlock")
def unlock_password(username: str | None, id: UUID | None):
    if username == None:
        return {"message": "Valid User name required"}
    elif valid_users.get(username) == None:
        return {"message": "User name does not exist"}
    else:
        if id == None:
            return {"message": "Valid token required"}
        else:
            user = valid_users.get(username)
            if user.id == id:
                return {"passord": user.password}
            else:
                return {"message": "Invalid Token"}

@app.get("level1/login/{username}/{password}")
def login_with_token(username:str, password:str, id:UUID):
    if valid_users.get(username) == None:
        return {"message": "Valid User name required"}
    else:
        user = valid_users.get(username)
        if user.id == id and checkpw(password.encode(), user.passphrase):
            return user
        else:
            return {"message": "Invalid User"}

@app.post("/level1/account/profile/add", response_model=UserProfile)
def add_profile(uname: str,
                fname: str = Form(...),
                lname: str = Form(...),
                mid_init: str = Form(...),
                user_age: int = Form(...),
                salary: float = Form(...),
                bday: str = Form(...),
                utype: UserType = Form(...),):
    if valid_users.get(uname) == None:
        return UserProfile(firstname=None, lastname=None, middle_initial=None, 
                           age=None, salary=None, birthday=None, user_type=None)
    else:
        profile = UserProfile(firstname=fname, lastname=lname, middle_initial=mid_init, 
                              age=user_age, salary=salary, birthday=bday, user_type=utype)
        valid_profiles[uname] = profile
        return profile

@app.put("/level1/account/profile/update/{username}")
def update_profile(username:str, id:UUID, new_profile: UserProfile):
    if valid_users.get(username) == None:
        return {"message": " Invalid User name"}
    else:
        user = valid_users.get(username)
        if user.id == id:
            valid_profiles = new_profile
        else:
            return {"message": "User does not exist"}

@app.patch("/level1/profile/update/names/{username}")
def update_profile_names(id: UUID, username: str = '', new_names: dict[str, str] =None):
    if valid_users.get(username) == None or new_names == None:
        return {"message": "User / Names not exists"}
    else:
        user = valid_users.get(username)
        if user.id == id:
            profile = valid_profiles[username]
            profile.firstname = new_names["fname"]
            profile.lastname = new_names["lname"]
            profile.middle_initial = new_names["mi"]
            valid_profiles[username] = profile
            return {"message": "Names successfully updated"}
        else:
            return {"message":"User Does not exist"}

@app.get("level1/account/profile/view/{username}")
def access_profile(username:str, id:UUID):
    if valid_users.get(username) == None:
        return {"messsage": "Unknow User"}
    else:
        user = valid_users.get(username)
        if user.id == id:
            profile = valid_profiles[username]
            return {"message": profile}
        else:
            return {"message": "User Profile does not exists"}

@app.post("/level1/discussion/posts/add/{username}")
def post_discussion(username: str, post: Post, post_type: PostType):
    if valid_users.get(username) == None:
        return {"message":"User Invalid"}
    elif not (discussion_posts.get(id) == None):
        return {"message": "Post already exists"}
    else:
        forum_post = ForumPost(id=uuid1(), topic=post.topic, message=post.message, 
                               post_type=post_type, date_posted=post.date_posted, username=username)
        user = valid_profiles[username]
        forum = ForumDiscussion(id=uuid1(), main_post=forum_post, author=user, replies=list())
        discussion_posts[forum.id] = forum
        return forum

@app.post("/level1/discussion/posts/reply/{username}")
def post_reply(username:str, id:UUID, post_type: PostType, post_reply: Post):
    if valid_users.get(username) == None:
        return {"message": "Invalid User"}
    elif discussion_posts.get(id) == None:
        return {"message": "Post Does not exist"}
    else:
        reply = ForumPost(id=uuid1(), topic=post_reply.topic, message=post_reply.message, 
                          post_type = post_type, date_posted=post_reply.date_posted, username=username)
        main_post = discussion_posts[id]
        main_post.replies.append(reply)
        return reply

@app.put("/level1/discussion/posts/update/{username}")
def update_discussion(username:str, id:UUID, post_type:PostType, post: Post):
    if valid_users.get(username) == None:
        return {"message": "Invalid User"}
    elif discussion_posts.get(id) == None:
        return {"message": "Post Does not exist"}
    else:
        forum_post = ForumPost(id=uuid1(), topic=post_reply.topic, message=post_reply.message,
                               post_type = post_type, date_posted=post_reply.date_posted, username=username)
        forum = discussion_posts[id]
        forum.main_post = forum_post
        return {"message": "main post update"}

@app.delete("/level/discusison/posts/remove/{username}")
def delete_discussion(username:str, id:UUID):
    if valid_users.get(username) == None:
        return {"message": "Invalid User"}
    elif discussion_posts.get(id) == None:
        return {"message": "Post Does not exist"}
    else:
        del discussion_posts[id]
        return {"message": "Post Deleted"}

@app.get("/level1/discussion/posts/view/{username}")
def view_discussion(username:str, id:UUID):
    if valid_users.get(username) == None:
        return {"message": "Invalid User"}
    elif discussion_posts.get(id) == None:
        return {"message": "Post Does not exist"}
    else:
        forum = discussion_posts[id]
        return forum

@app.get("/level1/headers/verify")
def verify_headers(host:str = Header(None),
                   accept:str = Header(None),
                   accept_language:str = Header(None),
                   accept_encoding:str = Header(None),
                   user_agent:str = Header(None)):
    request_headers["Host"] = host
    request_headers["Accept"] = accept
    request_headers["Accept-Language"] = accept_language
    request_headers["Accept-Encoding"] = accept_encoding
    request_headers["User-Agent"] = user_agent
    return request_headers

@app.get("/level1/login/cookies")
def access_cookies(userkey:str = Cookie(None),
                   identity:str = Cookie(None)):
    cookies["userkey"] = userkey
    cookies["identity"] = identity

@app.post("/level1/login/rememberme/create")
def create_cookies(resp: Response, id: UUID, username: str = ""):
    resp.set_cookie(key="userkey", value=username)
    resp.set_cookie(key="identity", value=str(id))
    return {"message": "remember-me tokens created"}







