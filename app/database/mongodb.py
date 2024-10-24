import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI and DB Name from environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME")

# MongoDB client and database
client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]

# Example collection
user_collection = db["users"]
