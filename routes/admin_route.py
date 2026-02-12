from fastapi import APIRouter,Request,HTTPException,status
from schemas.auth_schema import OutputResponse as output_schema
from utils.helperfunction_Obj_to_string import helperfunction_Object_to_string
from bson import ObjectId

router = APIRouter()

"""
================================
GET ALL USERS DETAIL FOR ADMIN DASHBOARD END POINT
================================
"""
@router.get('/get-user-details')
async def get_user_details(request:Request):
    authCollection=request.app.state.auth_collection
    data= await authCollection.find({}).to_list(length=None)
    all_users=[]
    for user in data:
        all_users.append(helperfunction_Object_to_string(user))

    return{
        "msg":"getting all the data",
        "users":all_users
    }

"""
================================
GET ALL AWAITING EMAIL FOR VERIFICATION FOR ADMIN DASHBOARD=> END POINT
================================
"""
@router.get('/awaiting-email-verification')
async def pending_email_for_verification(request:Request):
    pending_collection=request.app.state.pending_collection
    data=await pending_collection.find({}).to_list(length=None)
    all_awaiting_users=[]
    for awaited in data:
        awaited['_id']=str(awaited['_id'])
        all_awaiting_users.append(awaited)
    
    return{
        "msg":"Getting all awaiting users",
        "awaitedusers":all_awaiting_users
    }


"""
awaiting-email-verification
================================
GET ALL MESSAGE FROM CONTACT FORM FOR ADMIN DASHBOARD END POINT
================================
"""
@router.get("/get-messages")
async def get_messages(request:Request):
    contact_collection=request.app.state.contact_collection
    data= await contact_collection.find({}).to_list(length=None)
    all_message=[]
    for message in data:
        message['_id']=str(message['_id'])
        all_message.append(message)
    
    return{
        "msg":"getting all the message data",
        "queries":all_message
    }


"""
================================
DELETE MESSAGE OF A USER FROM ADMIN DASHBOARD
================================
"""
@router.delete('/delete-contact/{id}')
async def delete_contact(id:str,request:Request):
    contactCollection=request.app.state.contact_collection
    try:
       result=await contactCollection.find_one_and_delete({"_id":ObjectId(id)})
       print("Delete contact: ",result)
       return{
           "msg":"Message deleted successfully",
       }
    except Exception as e:
        print(f"Error occurd: {e}")
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,detail="database connection failed or internal server error")
    


