from pydantic import BaseModel, Field
from typing import Optional
from app.db import db  # Import the database setup

# MongoDB Prompt Data collection
prompt_data_collection = db["prompt_data"]


# Pydantic model for Prompt Data
class PromptData(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    data1: str  # First piece of data
    data2: str  # Second piece of data

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# MongoDB to Pydantic conversion helper
def prompt_data_helper(prompt_data) -> dict:
    return {
        "id": str(prompt_data["_id"]),
        "data1": prompt_data["data1"],
        "data2": prompt_data["data2"],
    }
