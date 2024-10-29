from pydantic import BaseModel, Field
from typing import Optional
from app.db import db  # Import the database setup

# MongoDB Client collection
client_collection = db["clients"]


# Pydantic model for Client
class Client(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    url: str  # Assuming URL is a string

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# MongoDB to Pydantic conversion helper
def client_helper(client) -> dict:
    return {"id": str(client["_id"]), "url": client["url"]}
