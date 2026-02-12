import os
from dotenv import load_dotenv
load_dotenv()
import bcrypt
from fastapi import APIRouter,Request,HTTPException,status
from schemas.auth_schema import OutputResponse as output_schema
from schemas.auth_schema import PendingRegistration as pendingRegistration_schema
from models.auth_model import UserINDB as  user_model
from schemas.auth_schema import VerifyOTP as verifyOTP_schema
from schemas.auth_schema import Login as login_schema
from schemas.auth_schema import ForgotPasswordVerificationCode as resetCode_schema
from schemas.auth_schema import ResetPassword as resetPassword_schema
from utils.generate_jwt_token import generate_jwt_token_for_user
from utils.sendgrid_mail_to_user import sendgrid_mail_to_user
from utils.hash_password import hashed_user_password
from utils.otp_generate import generate_otp
from utils.generate_session_id import generate_session_for_user
from bson import ObjectId
from datetime import datetime,timezone,timedelta

JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY','')

router=APIRouter()


"""
================================
REGISTER A USER END POINT
================================
"""
@router.post("/register")
async def register_user(request:Request,data:pendingRegistration_schema):
    pending_collection=request.app.state.pending_collection
    authCollection=request.app.state.auth_collection
    dict_data=dict(data)
    
    user_existance=await authCollection.find_one({"email":dict_data['email']})
    if user_existance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="User already exist with this email")
    
    # convert user password string --> in bytes
    user_password_bytes=dict_data['password'].encode('utf-8')

    # hashing password
    hash_password=hashed_user_password(user_password_bytes)
    
    # changing the password value by hass_password
    dict_data['password']=hash_password
    
    # OTP generation
    otp=generate_otp()
   
    # Adding otp field to save it temperory for verification
    dict_data['otp']=otp
    
    # user_model to save data in Database
    user_model_obj=user_model(**dict_data)

    created_user= await pending_collection.insert_one(user_model_obj.model_dump())
    
    email=dict_data['email']
    # Send email through to user by using Sendgrid
    sending_status=sendgrid_mail_to_user(email,otp)
    # sending_status=True
    inserted_id=str(created_user.inserted_id)

    if sending_status:
        return{
            "msg":"OTP sent successfully to your entered email",
            "id":inserted_id
        }
    else:
        return{
            "msg":"Something went wrong"
        }
    

"""
================================
VERIFY OTP TO REGISTER A USER 
================================
"""
@router.post("/verify-otp")
async def verify_otp(request:Request,otp_data:verifyOTP_schema):
    dict_otp_data=dict(otp_data)
    
    # data of registration has been saved in this collection for temporary
    pending_collection=request.app.state.pending_collection
    authCollection=request.app.state.auth_collection
    pending_user=await pending_collection.find_one({"email":dict_otp_data['email']})
    
    if not pending_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="OTP session has been expired !")

    if pending_user and pending_user['otp']==dict_otp_data['otp']:
        try:
            del pending_user['_id']
            del pending_user['otp']
            # Actual registration data saved in this auth collection
            await authCollection.insert_one(pending_user)
            delete_re=await pending_collection.delete_one({"email":dict_otp_data['email']})
    
            return{
                "msg":"Your account verified successfully",
            }
        except Exception as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Some thing went wrong in verifying otp")
    else:
        return{
            "msg":"OTP session expired or you entered wrong OTP !"
        }
   


"""
================================
LOGIN USER END POINT
================================
"""
@router.post("/login")
async def check_user_login_credential(request:Request,data:login_schema):
    authCollection=request.app.state.auth_collection
    dict_data=dict(data)
    user_input_password=dict_data['password']

    user_existance=await authCollection.find_one({"email":dict_data['email']})
    # check that user have already account or not
    if not user_existance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Sorry!😌 We couldn't find any account with this email")
    
    hashed_password_from_db=user_existance['password']
    
    # checking that user_input password is matched with corresponding password saved for that user
    ispassword_match=bcrypt.checkpw(user_input_password.encode('utf-8'),hashed_password_from_db.encode('utf-8'))
    if not ispassword_match:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Invalid user credential please try again!")

    session_id=generate_session_for_user()
    created_at=datetime.now(timezone.utc)
    await authCollection.update_one({"email":dict_data['email']},{"$set":{"session_id":session_id,"created_at":created_at}})
    # function which generate jwt_token
    jwt_token=generate_jwt_token_for_user(user_existance['email'],user_existance['role'],session_id,JWT_SECRET_KEY)
    
    return{
        "msg":"You are logged in successfully",
        "token":jwt_token,
        "details":{
            "id":str(user_existance['_id']),
            "email":user_existance['email'],
            }
        }

"""
================================
OTP CODE GENERATOR TO RESET PASSWORD
================================
"""
@router.post("/forgot-password/generate-code")
async def forgot_password_generate_code(request:Request,reset_code_data:resetCode_schema):
    resetcode_dict=dict(reset_code_data)
    pending_collection=request.app.state.pending_collection
    auth_collection=request.app.state.auth_collection
    email=resetcode_dict['email']
    user_existance=await auth_collection.find_one({"email":email})
    if not user_existance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Sorry!😌 We couldn't find any account with this email")
    
    pending_otp=await pending_collection.find_one({"email":email})
    if pending_otp:
        return{
            "msg":"Sorry! To generate OTP come after 5 minutes"
        }
    
    otp=generate_otp()
    resetcode_dict['otp']=otp
    created_user= await pending_collection.insert_one(resetcode_dict)
    
    # send the email to user for reset password with otp verification
    sending_status=sendgrid_mail_to_user(email,otp)

    if sending_status:
        return{
            "msg":"Success! We've sent a reset code (OTP) to your registered email to reset your password. Don't forget to check your spam!",
            "id":str(created_user.inserted_id)
        }
    else:
        return{
            "msg":"Something went wrong"
        }


"""
================================
OTP VERIFICATION TO RESET PASSWORD AND UPDATE USER NEW PASSWORD END POINT
================================
"""
@router.post("/reset-password")
async def reset_password(request:Request,reset_data:resetPassword_schema):
    auth_collection=request.app.state.auth_collection
    pending_collection=request.app.state.pending_collection
    resetdata_dict=dict(reset_data)
    account_existance=await auth_collection.find_one({"email":resetdata_dict['email']})
    if not account_existance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="Sorry!😌 We couldn't find any account with this email")
    
    # pending_reset 
    user_existance=await pending_collection.find_one({"email":resetdata_dict['email']})
    if not user_existance:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,detail="OTP session has been expired ! Or You didn't generate OTP yet")
    
    email=user_existance['email']
    user_password_bytes=resetdata_dict['password'].encode('utf')
    created_at=datetime.now()

    if user_existance and resetdata_dict['otp']==user_existance['otp']:
        # hashing the new password
        hash_password=hashed_user_password(user_password_bytes)
    
        # updating newpassword of user in db
        resul=await auth_collection.update_one({"email":email},{"$set":{"password":hash_password,"created_at":created_at}})

        # deleting the pending collection of OTP
        await pending_collection.delete_one({"email":email})

        return{
            "msg":"Your password has been updated now"
        }
    else:
        return{
            "msg":"OTP session expired or you entered wrong OTP !"
        }

    


        
        



    
    









# delete a user
@router.delete("/delete-user/{id}")
async def delete_user(id:str,request:Request):
    authCollection=request.app.state.auth_collection
     
    result=await authCollection.find_one_and_delete({"_id":ObjectId(id)})
    return{
        "msg":"User deleted successfully",
        "email":str(result['email'])
    }
