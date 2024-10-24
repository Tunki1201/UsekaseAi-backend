from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from database.mongodb import db  # Import the database setup

# MongoDB Account collection
account_collection = db["accounts"]


# Pydantic model for Account
class Account(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    client_id: ObjectId  # Reference to Client ID from the Client database
    user_id: ObjectId  # Reference to User ID from the User database

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# MongoDB to Pydantic conversion helper
def account_helper(account) -> dict:
    return {
        "id": str(account["_id"]),
        "client_id": account["client_id"],
        "user_id": account["user_id"],
    }
