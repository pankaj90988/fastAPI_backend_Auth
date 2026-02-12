from pydantic import BaseModel,EmailStr,Field
from datetime import datetime,timezone

"""
================================
SCHEMA TO VALIDATE CONTACT FORM
================================
"""
class Contact(BaseModel):
    username:str=Field(...,description="username is required")
    email:EmailStr=Field(...,description="Email is required")
    message:str = Field(...,description="Reqiure if he/she want to contact",max_length=200)
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))
