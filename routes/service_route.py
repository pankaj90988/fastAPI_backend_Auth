from fastapi import APIRouter,Request,Depends,HTTPException,status
from schemas.service_schema import Service as service_model
from typing import List
from schemas.service_schema import helperfunction_Object_to_string_service
from utils.route_security import oauth2_schema
from utils.decode_jwt_token import decode_user_token

router=APIRouter()


"""
================================
GET SERVICE PAGE DATA END POINT
================================
"""
@router.get("/service")
async def get_services(request:Request,token:str=Depends(oauth2_schema)):
    payload=decode_user_token(token)
    auth_collection= request.app.state.auth_collection
    if payload:
        session_id=payload.get('session_id')
        user_email=payload.get('sub')
        user_details=await auth_collection.find_one({"email":user_email})
        db_session_id=user_details['session_id']
        if session_id!=db_session_id:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="Unauthorized access, A new device login was detected for this account!")
    
    service_collection=request.app.state.service_collection
    service_data= await service_collection.find({}).to_list(length=None)
    all_service=[]
    for service in service_data:
        all_service.append(helperfunction_Object_to_string_service(service))
    return{
        "message":all_service
    }


"""
================================
ADD A NEW SERVICE END POINT
================================
"""
@router.post("/add-service-details")
async def add_new_services(service_data:List[service_model],request:Request):
    service_collection=request.app.state.service_collection
    dict_service=[]
    for data in service_data:
        dict_service.append(dict(data))

    inserte_data=await service_collection.insert_many(dict_service)
    return{
        "msg":"data added successfully"
    }
    


    