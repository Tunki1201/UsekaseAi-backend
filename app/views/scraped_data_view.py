from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.scraped_data_model import ScrapedData
from app.controllers import scraped_data_controller
from app.schema import ValidateUrlExists

router = APIRouter()


# GET all scraped data
@router.get("/get/", response_model=List[ScrapedData])
async def get_scraped_data():
    return await scraped_data_controller.get_all_scraped_data()


# GET a specific scraped data entry by ID
@router.get("/get/{id}", response_model=ScrapedData)
async def get_scraped_data_entry(id: str):
    scraped_data = await scraped_data_controller.get_scraped_data_by_id(id)
    if scraped_data is None:
        raise HTTPException(status_code=404, detail="Scraped data not found")
    return scraped_data


# POST: Create a new scraped data entry
@router.post("/create/", response_model=ScrapedData)
async def create_scraped_data_entry(data: ScrapedData):
    return await scraped_data_controller.create_scraped_data(data)


# PUT: Update a scraped data entry by ID
@router.put("/update/{id}", response_model=ScrapedData)
async def update_scraped_data_entry(id: str, data: ScrapedData):
    updated_data = await scraped_data_controller.update_scraped_data(id, data)
    if updated_data is None:
        raise HTTPException(status_code=404, detail="Scraped data not found")
    return updated_data


# DELETE: Delete a scraped data entry by ID
@router.delete("/delete/{id}")
async def delete_scraped_data_entry(id: str):
    deleted = await scraped_data_controller.delete_scraped_data(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Scraped data not found")
    return {"status": "Scraped data deleted"}


# New endpoint to validate URL existence
@router.get("/check-url/")
async def validate_url_exists(
    url: str = Query(..., description="URL to check")  # Accept URL as query parameter
):
    """
    Endpoint to validate if a URL exists in the website_content of ScrapedData.
    """
    try:
        # Call the controller function to check URL existence
        result = await scraped_data_controller.check_url_exists(url)

        if isinstance(result, dict) and "company_url" in result:
            # If the URL already exists, return the existing data
            return {
                "exists": True,
                "message": "URL already exists in the database.",
                "company_data": result,  # Existing data
            }
        elif (
            isinstance(result, dict)
            and "message" in result
            and "company_data" in result
        ):
            # If new data was inserted successfully
            return {
                "exists": False,
                "message": result["message"],
                "company_data": result.get("company_data", {}),
            }
        else:
            # In case the result is not as expected, return a generic message
            return {"exists": False, "message": "Unable to validate URL at the moment."}

    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(status_code=500, detail=f"Error checking URL: {str(e)}")
