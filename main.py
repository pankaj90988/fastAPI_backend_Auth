from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.db import connect_DB,get_db,close_db_connection
from routes.auth_route import router as auth_route
from routes.contact_route import router as contact_route
from routes.service_route import router as service_route
from routes.admin_route import router as admin_route
from routes.verifySession_route import router as verifySession_route
from fastapi.middleware.cors import CORSMiddleware


"""
================================
LIFE SPAN FUNCTION / STARTUP AND SHUTDOWN FUNCTION
================================
"""
@asynccontextmanager
async def life_span(app:FastAPI):
    print("Starting server..")

    try:
       await connect_DB()
       db_name=get_db()
       app.state.auth_collection=db_name['users']
       app.state.contact_collection=db_name['contacts']
       app.state.service_collection=db_name['services']
       app.state.pending_collection=db_name['pending_registration']
    #    await app.state.pending_collection.drop_index('created_at_1')
       await app.state.pending_collection.create_index('created_at',expireAfterSeconds=300)
    except Exception as e:
        print(f"Error occur at startup:{e}")

    yield

    try:
        close_db_connection()
        print("Server shut down successfully")
    except Exception as e:
        print(f"Error occur during server shutdown: {e}")
        
app=FastAPI(
    lifespan=life_span,
    # docs_url=None,
    # redoc_url=None,
    # openapi_url=None
) #FastAPI Instance


"""
================================
ADDING MIDDLEWARE TO HANDLE THE CORS POLICY ERROR /
DESCRIBED THAT FROM WHICH ORIGIN BACKEND ACCEPT THE REQUEST AND RESPOND IT
================================
"""
# origins = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173"
# ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

"""
================================
BINDING ALL ROUTERS WITH FAST API INSTANCE WHIC IS ENTRY POINT OF FASTAPI APP
================================
"""
app.include_router(auth_route,tags=['Authentication'],prefix="/api/auth")
app.include_router(contact_route,tags=['Contact'],prefix="/api/form")
app.include_router(service_route,tags=['Services'],prefix="/api/data")
app.include_router(verifySession_route,tags=['Check_Token_Session'],prefix="/api")
app.include_router(admin_route,tags=['Admin_Panel'],prefix='/api/admin-dashboard')

@app.get("/")
async def root():
    return{
        "msg":"Server is live now.."
    }