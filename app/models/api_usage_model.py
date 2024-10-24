from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from database.mongodb import db  # Import the database setup

# MongoDB API Usage collection
api_usage_collection = db["api_usage"]


# Pydantic model for API Usage
class APIUsage(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: ObjectId  # Reference to User ID
    endpoint: str  # The API endpoint being used
    request_count: int  # Number of requests made to this endpoint
    timestamp: str  # Time when the usage was recorded

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# MongoDB to Pydantic conversion helper
def api_usage_helper(api_usage) -> dict:
    return {
        "id": str(api_usage["_id"]),
        "user_id": api_usage["user_id"],
        "endpoint": api_usage["endpoint"],
        "request_count": api_usage["request_count"],
        "timestamp": api_usage["timestamp"],
    }
