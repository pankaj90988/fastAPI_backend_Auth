from fastapi import APIRouter,Request,HTTPException,Depends,status
from schemas.contact_schema import Contact as contact_model
from utils.route_security import oauth2_schema
from utils.decode_jwt_token import decode_user_token

router=APIRouter()

"""
================================
CONTACT FORM END POINT
================================
"""
@router.post("/contact")
async def create_contact_detail(request:Request,contact_data:contact_model,token:str=Depends(oauth2_schema)):
    payload=decode_user_token(token)
    auth_collection= request.app.state.auth_collection
    if payload:
        session_id=payload.get('session_id')
        user_email=payload.get('sub')
        user_details=await auth_collection.find_one({"email":user_email})
        db_session_id=user_details['session_id']
        if session_id!=db_session_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Unauthorized access, A new device login was detected for this account!")
        
    contactCollection=request.app.state.contact_collection
    dict_contact=dict(contact_data)
    result=await contactCollection.insert_one(dict_contact)
    
    find_contact=await contactCollection.find_one({"_id":result.inserted_id})
    return{
        "msg":"Response saved successfully",
        "id":str(find_contact['_id']),
        # "message":find_contact['message']
    }


