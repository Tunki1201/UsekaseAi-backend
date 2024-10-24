from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from database.mongodb import db  # Import the database setup

# MongoDB Error Log collection
error_log_collection = db["error_logs"]


# Pydantic model for Error Log
class ErrorLog(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    error_message: str  # Description of the error
    timestamp: str  # Time when the error occurred
    report_id: ObjectId  # Optional reference to Report ID
    user_id: ObjectId  # Optional reference to User ID

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# MongoDB to Pydantic conversion helper
def error_log_helper(error_log) -> dict:
    return {
        "id": str(error_log["_id"]),
        "error_message": error_log["error_message"],
        "timestamp": error_log["timestamp"],
        "report_id": error_log.get("report_id"),
        "user_id": error_log.get("user_id"),
    }
