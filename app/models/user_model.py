from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.db import db

# MongoDB Chapter collection
user_collection = db["users"]
# Pydantic model
class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    email: str
    first_name: str
    last_name: str
    imageUrl: Optional[str]
    auth_provider: str
    is_authenticated: bool = False
    client_id: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    modified_at: datetime = Field(default_factory=datetime.utcnow)
    role: Optional[str]
    team: Optional[str]
    credits_purchased: Optional[int] = 0

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda v: v.isoformat()}


# MongoDB to Pydantic conversion helper
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "avatar": user.get("avatar"),
        "auth_provider": user["auth_provider"],
        "is_authenticated": user["is_authenticated"],
        "client_id": user.get("client_id"),
        "created_at": user["created_at"],
        "modified_at": user["modified_at"],
        "role": user.get("role"),
        "team": user.get("team"),
        "credits_purchased": user.get("credits_purchased", 0),
    }
