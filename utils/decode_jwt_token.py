from fastapi import HTTPException,status
import jwt
import os
from dotenv import load_dotenv
load_dotenv()

JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY',"")

def decode_user_token(token:str):
    try:
        payload=jwt.decode(token,JWT_SECRET_KEY,algorithms="HS256")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='Token has been expired !')
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='Invalid token, Denied access !')

