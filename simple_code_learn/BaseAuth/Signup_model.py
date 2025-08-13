from pydantic import BaseModel, ConfigDict
from datetime import date


class SignupReq(BaseModel):
    id : int
    username: str
    password: str
    model_config = ConfigDict(from_attributes=True) # inform pydantic to read data from ORM Objects

class ProfileReq(BaseModel):
    id:int
    firstname:str
    lastname:str
    age:int
    membership_date : date
    member_type:str
    login_id:int
    status:int
    model_config = ConfigDict(from_attributes=True) # inform pydantic to read data from ORM Objects
