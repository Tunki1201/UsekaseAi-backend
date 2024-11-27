from http.client import HTTPException
from app.utils import fetch_company_info
from bson import ObjectId
from app.models.scraped_data_model import (
    CompanyWebsiteContents,
    KeyActivity,
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


async def check_url_exists(url: str) -> bool:
    """
    Check if a URL already exists in the website_content field of the ScrapedData collection.
    """
    try:
        print("------------------------------url:", url)
        # Query the MongoDB collection for a matching URL in the `website_content.url` field
        exists = await scraped_data_collection.find_one({"company_url": url})

        print(exists)
        # If a matching document is found, return True
        if exists is not None:
            return exists

        # If the URL doesn't exist, call the external API
        company_name = ""  # Replace with dynamic logic to get the company name
        company_background = ""  # Replace with dynamic logic if needed
        company_data = fetch_company_info(url, company_name, company_background)

        if company_data:
            # Map the API response to the ScrapedData model
            scraped_data = ScrapedData(
                company_url=company_data.get("company_url"),
                company_name=company_data.get("company_name"),
                company_background=company_data.get("company_background"),
                company_industries=company_data.get("company_industry", []),
                linkedin_url=company_data.get("linkedin_profile"),
                glassdoor_url=company_data.get("glassdoor_profile"),
                company_website_contents=[
                    CompanyWebsiteContents(
                        url=content["url"],
                        title=content.get("raw_content", "").split("\n")[
                            1
                        ],  # Extract title from the second line (after the first newline)
                        content=content.get("raw_content", "")
                        .split("\n", 1)[1]
                        .strip(),  # Extract content after the first newline
                    )
                    for content in company_data.get("company_website_contents", [])
                ],
                key_activities=[
                    KeyActivity(
                        activity=activity["activity"],
                        value_chain_area=activity["value_chain_area"],
                        ai_applicability_score=activity["ai_applicability_score"],
                    )
                    for activity in company_data.get("value_chain_activities", {}).get(
                        "key_activities", []
                    )
                ],
            )

            result = await scraped_data_collection.insert_one(
                scraped_data.dict(by_alias=True)
            )

        if result.id:
            print(f"Data for {company_data['company_name']} inserted successfully.")
            return {
                "message": "Data inserted successfully",
                "company_data": company_data,
            }
        else:
            raise HTTPException(
                status_code=500, detail="Failed to save data to the database"
            )

    except Exception as e:
        # Log and handle potential exceptions
        print(f"Error checking URL existence: {e}")
        raise e  # Re-raise exception to handle it at a higher level if needed
