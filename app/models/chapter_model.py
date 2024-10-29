from pydantic import BaseModel, Field
from typing import Optional, List
from app.db import db  # Import the database setup

# MongoDB Chapter collection
chapter_collection = db["chapters"]


# Pydantic model for Chapter
class Chapter(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    text: List[str]  # List of text entries in the chapter
    quote: Optional[str]  # A quote related to the chapter
    graph: Optional[str]  # A string URL or description for the graph
    image: Optional[str]  # A string URL for the image
    table: Optional[str]  # A string URL or description for the table

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# MongoDB to Pydantic conversion helper
def chapter_helper(chapter) -> dict:
    return {
        "id": str(chapter["_id"]),
        "text": chapter["text"],
        "quote": chapter.get("quote"),
        "graph": chapter.get("graph"),
        "image": chapter.get("image"),
        "table": chapter.get("table"),
    }
