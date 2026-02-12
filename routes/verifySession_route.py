from fastapi import APIRouter,Depends,Request,HTTPException,status
from utils.route_security import oauth2_schema
from utils.decode_jwt_token import decode_user_token

router=APIRouter()


"""
================================
VERIFICATION OF SESSION ID AND CHECK TOKEN VALIDATION END POINT
================================
"""
@router.get("/verify-session")
async def verify_session(request:Request,token:str=Depends(oauth2_schema)):
      
      payload=decode_user_token(token)
      auth_collection=request.app.state.auth_collection
      session_id=payload.get('session_id')
      email=payload.get('sub')
      print(email)
      
      user=await auth_collection.find_one({"email":email})
      if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND,detail='User not found')
      
      db_session_id=user['session_id']
      print("session id: ",db_session_id)
      if session_id != db_session_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail='Unauthorized access, A new device login was detected for this account! from bc')
      
      return{
            "msg":"Everything is fine"
      }

      
      

