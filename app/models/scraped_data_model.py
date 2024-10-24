from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId  # Import ObjectId
from database.mongodb import db  # Import the database setup

# MongoDB Scraped Data collection
scraped_data_collection = db["scraped_data"]


# Pydantic model for Website Content
class WebsiteContent(BaseModel):
    url: str  # URL of the website
    title: str  # Title of the website
    content: str  # Content of the website


# Pydantic model for Scraped Data
class ScrapedData(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    client_id: ObjectId  # Reference to Client ID (as ObjectId)
    name: str  # Name of the entity
    legal_name: Optional[str]  # Legal name of the entity
    time_scraped: Optional[str]  # Time when data was scraped
    website_content: WebsiteContent  # Content of the website
    primary_industry: Optional[str]  # Primary industry of the entity
    secondary_industry: Optional[str]  # Secondary industry of the entity
    key_activities: Optional[str]  # Key activities of the entity
    linkedin_url: Optional[str]  # LinkedIn URL
    glassdoor_url: Optional[str]  # Glassdoor URL
    leadership_url: Optional[str]  # Leadership URL
    background_info: Optional[str]  # Background information
    og_description: Optional[str]  # Open Graph description
    og_title: Optional[str]  # Open Graph title
    og_image: Optional[str]  # Open Graph image URL

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# MongoDB to Pydantic conversion helper
def scraped_data_helper(scraped_data) -> dict:
    return {
        "id": str(scraped_data["_id"]),
        "client_id": str(
            scraped_data["client_id"]
        ),  # Convert ObjectId to string for output
        "name": scraped_data["name"],
        "legal_name": scraped_data.get("legal_name"),
        "time_scraped": scraped_data.get("time_scraped"),
        "website_content": {
            "url": scraped_data["website_content"]["url"],
            "title": scraped_data["website_content"]["title"],
            "content": scraped_data["website_content"]["content"],
        },
        "primary_industry": scraped_data.get("primary_industry"),
        "secondary_industry": scraped_data.get("secondary_industry"),
        "key_activities": scraped_data.get("key_activities"),
        "linkedin_url": scraped_data.get("linkedin_url"),
        "glassdoor_url": scraped_data.get("glassdoor_url"),
        "leadership_url": scraped_data.get("leadership_url"),
        "background_info": scraped_data.get("background_info"),
        "og_description": scraped_data.get("og_description"),
        "og_title": scraped_data.get("og_title"),
        "og_image": scraped_data.get("og_image"),
    }
