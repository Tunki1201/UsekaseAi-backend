from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from database.mongodb import db  # Import the database setup

# MongoDB Report collection
report_collection = db["reports"]


# Pydantic model for Report
class Report(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    number: str
    chapters: List[str]  # Assuming chapters is a list of strings
    delayed_time: Optional[int] = 0  # Optional int representing delayed time in minutes
    tone: Optional[str]  # Tone of the report
    downloaded: bool = False  # Boolean indicating if the report has been downloaded
    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )  # Auto-generated timestamp
    client_id: ObjectId  # Foreign key relation to the Client entity
    account_id: ObjectId  # Foreign key relation to the Account entity

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda v: v.isoformat()}


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
