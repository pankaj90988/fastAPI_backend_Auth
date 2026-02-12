import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

# it will load the dotenv file
load_dotenv()

client:AsyncIOMotorClient | None = None
MONGO_URI=os.getenv('MONGO_URI'," ")
DATABASE_NAME=os.getenv('DATABASE_NAME'," ")


"""
================================
FUNCTION WHICH CONNECT SERVER WITH MONGO CLIENT
================================
"""
async def connect_DB():
    global client
    print("Connecting to database....")
    client=AsyncIOMotorClient(MONGO_URI,ServerSelectionTimeoutMs=5000)
    try:
        await client.admin.command('ping')
        print("Database is connected successfully with server")
    except ServerSelectionTimeoutError as e:
        print("Conection failed to database:",e)
        raise(e)



"""
================================
FUNCTION WHICH WILL RETURN DATABASE NAME
================================
"""
def get_db():
    global client
    if client is None:
        raise Exception('Not connect to database')
    return client[DATABASE_NAME]


"""
================================
FUNCTION WHICH CLOSE THE DB CONNECTION
================================
"""
def close_db_connection():
    print("Server is shutting down..")
    global client
    if client:
        client.close()
        print(f"Database disconnected with server....")
        client=None
    else:
        print(f"Client Object is found None")

