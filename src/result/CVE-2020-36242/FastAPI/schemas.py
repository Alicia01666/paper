from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    email: str
    

class UserCreate(UserBase):
    username : str

class User(UserCreate):
    uid: int
    reg_date: datetime.datetime
    exp_date: datetime.datetime

    class Config:
        orm_mode = True