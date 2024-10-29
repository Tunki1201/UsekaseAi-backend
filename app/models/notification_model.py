from pydantic import BaseModel, Field
from typing import Optional
from app.db import db  # Import the database setup

# MongoDB Notifications collection
notification_collection = db["notifications"]


# Pydantic model for Notifications
class Notification(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: str  # Reference to User ID
    message: str  # The notification message
    is_read: bool = False  # Indicates if the notification has been read
    created_at: str  # Time when the notification was created

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# MongoDB to Pydantic conversion helper
def notification_helper(notification) -> dict:
    return {
        "id": str(notification["_id"]),
        "user_id": notification["user_id"],
        "message": notification["message"],
        "is_read": notification["is_read"],
        "created_at": notification["created_at"],
    }
