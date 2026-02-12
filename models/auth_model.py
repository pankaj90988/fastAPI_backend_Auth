from pydantic import BaseModel,EmailStr,Field
from datetime import datetime,timezone


"""
================================
USERMODEL => DATA STRUCTURE WHICH WILL SAVE IN DATABASE
================================
"""
class UserINDB(BaseModel):
    username:str
    email:EmailStr
    phone:str
    password:str
    otp:str
    role:str=Field(default='user')
    session_id:str | None=Field(default=None)
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))