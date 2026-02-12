from pydantic import BaseModel,EmailStr,Field
from datetime import datetime,timezone
from typing import List


"""
================================
SCHEMA FOR USER DETAILS WHICH COME AS RESPONSE FOR ADMIN DASHBOARD
================================
"""
class UserDetail(BaseModel):
    id:str=Field(...,description="required")
    username:str=Field(..., description="Username is required to register")
    email:EmailStr=Field(...,description="Email is required to register")
    phone:str=Field(...,description="Phone number is required to register",max_length=10,min_length=10)
    created_at:datetime=datetime.now()
 
"""
================================
OUTPUT RESPONSE SCHEMA TO VALIDATE THE OUTPUT RESPONSE TO PREVENT THE SENSITIVE INFORMATION
================================
"""
class OutputResponse(BaseModel):
    users:List[UserDetail]
    

"""
================================
SCHEMA FOR LOGIN
================================
"""
class Login(BaseModel):
    email:EmailStr=Field(...,description="Email is required for verification")
    password:str=Field(...,description="Password is required for verification")


"""
================================
SCHEMA FOR REGISTERATOIN WHICH WE WILL FIRSTLY SAVE IN PENDING COLLECTION
================================
"""
class PendingRegistration(BaseModel):
    username:str=Field(..., description="Username is required to register")
    email:EmailStr=Field(...,description="Email is required to register")
    phone:str=Field(...,description="Phone number is required to register",max_length=10,min_length=10)
    password:str=Field(...,description="Password is required to register")


"""
================================
SCHEMA FOR OTP VERIFICATION FOR SUCCESSFULL REGISTRATION
================================
"""
class VerifyOTP(BaseModel):
    email:EmailStr=Field(...,description="Email is required for otp verification")
    otp:str=Field(...,description="OTP is required to verify users actual existance")


"""
================================
EMAIL VALIDATION TO SEND OTP FOR FORGOT PASSWORD
================================
"""
class ForgotPasswordVerificationCode(BaseModel):
    email:EmailStr=Field(...,description="Email is required to send the otp")
    created_at:datetime=Field(default_factory=lambda:datetime.now(timezone.utc))

 
"""
================================
SCHEMA TO VERIFY OTP AND UPDATE NEW PASSWORD => RESET PASSWORD
================================
"""
class ResetPassword(BaseModel):
    email:EmailStr=Field(...,description="Required for password reset")
    password:str=Field(...,description="New password is required for password reset")
    otp:str=Field(...,description="OTP is required for verification to reset password")