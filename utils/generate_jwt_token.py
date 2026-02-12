from datetime import datetime,timezone,timedelta
import jwt

def generate_jwt_token_for_user(user_email:str,user_role:str,session_id:str,JWT_SECRET_KEY:str):
    # JWT token creation 
    payload={
        "sub":user_email,
        "role":user_role,
        "session_id":session_id,
        "iat":datetime.now(timezone.utc),
        "exp":datetime.now(timezone.utc)+timedelta(hours=12)
    }
    jwt_token=jwt.encode(payload,JWT_SECRET_KEY,algorithm="HS256")
    return jwt_token
