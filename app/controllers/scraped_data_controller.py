from http.client import HTTPException
from bson import ObjectId
from app.utils.scrapping_engine import fetch_company_info
from app.models.scraped_data_model import (
    CompanyWebsiteContents,
    KeyActivity,
    scraped_data_collection,
    scraped_data_helper,
    ScrapedData,
)

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


async def check_url_exists(url: str) -> str:
    """
    Check if a URL already exists in the ScrapedData collection.
    """
    try:
        # Query MongoDB for a matching URL
        exists = await scraped_data_collection.find_one({"company_url": url})

        if exists is not None:
            return exists  # URL exists

        # If the URL doesn't exist, call the external API
        company_name = ""  # Replace with logic to get the company name dynamically
        company_background = (
            ""  # Replace with logic to get company background dynamically
        )
        company_data = fetch_company_info(url, company_name, company_background)

        # print("---------------------------------------------------", url, company_data)
        if company_data:
            # Prepare ScrapedData model for insertion
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
                        title=content.get("raw_content", "").split("\n")[1],
                        content=content.get("raw_content", "")
                        .split("\n", 1)[1]
                        .strip(),
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

            # Insert the data into MongoDB
            result = await scraped_data_collection.insert_one(
                scraped_data.dict(by_alias=True)
            )

            print("---------------------------------------------------", result)
            if result:
                return result  # Indicate new data insertion
            else:
                raise HTTPException(
                    status_code=500, detail="Failed to save data to the database."
                )

    except Exception as e:
        # Log and handle potential exceptions
        print(f"Error checking URL existence: {e}")
        raise e


async def get_company_info(url: str):
    """
    Fetch company information based on the given URL.
    """
    try:
        # Query MongoDB to find a matching document by company_url
        document = await scraped_data_collection.find_one({"company_url": url})

        if not document:
            # If no matching document is found, return None
            return None

        # Convert ObjectId to string if needed
        if "_id" in document:
            document["_id"] = str(document["_id"])

        return document

    except Exception as e:
        # Log or handle the exception as needed
        raise HTTPException(
            status_code=500, detail=f"Error fetching company info: {str(e)}"
        )
