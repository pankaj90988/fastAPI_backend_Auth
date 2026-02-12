from pydantic import BaseModel,Field
from datetime import datetime

"""
================================
SCHEMA TO VALIDATE SERVICE
================================
"""
class Service(BaseModel):
    service:str=Field(...,description="it contains services name")
    description:str=Field(...,description="details about service")
    price:str=Field(...,description="contains service price")
    provider:str=Field(...,description="contains provider details")
    image:str=Field(...,description="contains image url to corresponding service")
    created_at:datetime=datetime.now()


def helperfunction_Object_to_string_service(service):
     return{
        "_id":str(service['_id']),
        "service":service['service'],
        "description":service['description'],
        "price":service['price'],
        "provider":service['provider'],
        "image":service['image'],
        "created_at":service['created_at']
    }