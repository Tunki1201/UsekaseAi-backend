from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from database.mongodb import db  # Import the database setup

# MongoDB Audit Log collection
audit_log_collection = db["audit_logs"]


# Pydantic model for Audit Log
class AuditLog(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: ObjectId  # Reference to User ID
    action: str  # Description of the action performed
    timestamp: str  # Time when the action occurred
    details: Optional[str]  # Optional details about the action

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# MongoDB to Pydantic conversion helper
def audit_log_helper(audit_log) -> dict:
    return {
        "id": str(audit_log["_id"]),
        "user_id": audit_log["user_id"],
        "action": audit_log["action"],
        "timestamp": audit_log["timestamp"],
        "details": audit_log.get("details"),
    }
