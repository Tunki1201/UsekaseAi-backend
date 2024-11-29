from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from datetime import datetime
from app.db import db  # Import the database setup

# MongoDB Report collection
report_collection = db["reports"]


# Pydantic model for Report
class Report(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    number: str = "RPT-DEFAULT"  # Default number if not provided
    chapters: Dict[str, str] = Field(default_factory=dict)  # Default empty dict for chapters
    delayed_time: Optional[int] = 0
    tone: Optional[str] = "neutral"  # Default tone
    downloaded: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    client_id: str = "UNKNOWN_CLIENT"  # Default client ID as a string
    account_id: str = "UNKNOWN_ACCOUNT"  # Default account ID as a string
    company_url: str = ""
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            ObjectId: str,  # Convert ObjectId to string
        }


# MongoDB to Pydantic conversion helper
def report_helper(report) -> dict:
    return {
        "id": str(report["_id"]),
        "number": report["number"],
        "chapters": report["chapters"],
        "delayed_time": report.get("delayed_time", 0),
        "tone": report.get("tone"),
        "downloaded": report["downloaded"],
        "created_at": report["created_at"],
        "client_id": report["client_id"],
        "account_id": report["account_id"],
    }
