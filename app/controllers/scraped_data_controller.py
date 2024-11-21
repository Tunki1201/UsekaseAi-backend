from bson import ObjectId
from app.models.scraped_data_model import (
    scraped_data_collection,
    scraped_data_helper,
    ScrapedData,
)
from app.schema import ValidateUrlExists

# CRUD Operations for Scraped Data


# Get all scraped data
async def get_all_scraped_data():
    scraped_data_list = await scraped_data_collection.find().to_list(1000)
    return [scraped_data_helper(data) for data in scraped_data_list]


# Get a specific scraped data entry by ID
async def get_scraped_data_by_id(id: str):
    scraped_data = await scraped_data_collection.find_one({"_id": ObjectId(id)})
    if scraped_data:
        return scraped_data_helper(scraped_data)
    return None


# Create a new scraped data entry
async def create_scraped_data(data: ScrapedData):
    data_dict = data.dict(by_alias=True)
    new_data = await scraped_data_collection.insert_one(data_dict)
    created_data = await scraped_data_collection.find_one({"_id": new_data.inserted_id})
    return scraped_data_helper(created_data)


# Update an existing scraped data entry by ID
async def update_scraped_data(id: str, data: ScrapedData):
    updated_data = await scraped_data_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_data:
        return scraped_data_helper(updated_data)
    return None


# Delete a scraped data entry by ID
async def delete_scraped_data(id: str):
    result = await scraped_data_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0

# Function to check if a URL exists in website_content
async def check_url_exists(url: ValidateUrlExists) -> bool:
    """Check if a URL already exists in the website_content field of the ScrapedData collection."""
    exists = await scraped_data_collection.find_one({"website_content.url": url})
    return exists is not None