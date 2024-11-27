from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId  # Import ObjectId
from app.db import db  # Import the database setup

# MongoDB Scraped Data collection
scraped_data_collection = db["scraped_data"]


# Pydantic model for Website Content
class CompanyWebsiteContents(BaseModel):
    url: str  # URL of the website
    title: str  # Title of the website
    content: str  # Content of the website


# Pydantic model for Key Activity
class KeyActivity(BaseModel):
    activity: str  # Activity description
    value_chain_area: str  # Value chain area (e.g., Operations, Marketing)
    ai_applicability_score: int  # AI applicability score


class ScrapedData(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    company_url: str
    client_id: ObjectId = None  # Reference to Client ID (as ObjectId)
    company_name: str  # Name of the entity
    legal_name: Optional[str] = (
        None  # Make legal_name optional with a default value of None
    )
    time_scraped: Optional[str] = (
        None  # Make time_scraped optional with a default value of None
    )
    company_website_contents: List["CompanyWebsiteContents"]  # Content of the website
    company_industries: List[str]  # Primary industry of the entity
    secondary_industry: Optional[str] = (
        None  # Make secondary_industry optional with a default value of None
    )
    key_activities: Optional[List["KeyActivity"]] = None  # List of key activities
    linkedin_url: Optional[str] = None  # LinkedIn URL
    glassdoor_url: Optional[str] = None  # Glassdoor URL
    leadership_url: Optional[str] = None  # Leadership URL
    company_background: Optional[str] = None  # Background information
    og_description: Optional[str] = None  # Open Graph description
    og_title: Optional[str] = None  # Open Graph title
    og_image: Optional[str] = None  # Open Graph image URL

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
        "company_name": scraped_data["company_name"],
        "legal_name": scraped_data.get("legal_name"),
        "time_scraped": scraped_data.get("time_scraped"),
        "company_website_contents": {
            "url": scraped_data["company_website_contents"]["url"],
            "title": scraped_data["company_website_contents"]["title"],
            "content": scraped_data["company_website_contents"]["content"],
        },
        "company_industries": scraped_data.get("company_industries", []),
        "secondary_industry": scraped_data.get("secondary_industry"),
        "key_activities": [
            {
                "activity": activity["activity"],
                "value_chain_area": activity["value_chain_area"],
                "ai_applicability_score": activity["ai_applicability_score"],
            }
            for activity in scraped_data.get("key_activities", [])
        ],
        "linkedin_url": scraped_data.get("linkedin_url"),
        "glassdoor_url": scraped_data.get("glassdoor_url"),
        "leadership_url": scraped_data.get("leadership_url"),
        "company_background": scraped_data.get("company_background"),
        "og_description": scraped_data.get("og_description"),
        "og_title": scraped_data.get("og_title"),
        "og_image": scraped_data.get("og_image"),
    }
