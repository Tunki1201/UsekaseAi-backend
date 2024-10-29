# app/db.py
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]  # Access the specific database

# Example function to get collection
def get_collection(collection_name: str):
    return db[collection_name]

# Close connection (optional, e.g., for app shutdown)
async def close_connection():
    client.close()
