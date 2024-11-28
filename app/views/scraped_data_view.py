from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.scraped_data_model import ScrapedData
from app.controllers import scraped_data_controller

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
            # If the URL already exists
            return {"exists": True, "message": "URL already exists in the database."}
        elif isinstance(result, str) and result == "inserted":
            # If a new entry was successfully inserted
            return {
                "exists": False,
                "message": "URL did not exist; new data inserted successfully.",
            }
        else:
            # Unexpected result
            return {"exists": False, "message": "Unable to validate URL at the moment."}

    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(status_code=500, detail=f"Error checking URL: {str(e)}")


@router.get("/get-company-info/")
async def get_company_info(url: str = Query(..., description="URL to look up")):
    """
    Endpoint to fetch full company information based on the provided company URL.
    """
    try:
        # Call the controller to fetch data
        document = await scraped_data_controller.get_company_info(url)

        if not document:
            # Return a 404 error if the URL is not found
            raise HTTPException(status_code=404, detail="Company URL not found")

        # Return the entire document as-is
        return document

    except Exception as e:
        # Handle any unexpected errors
        raise HTTPException(
            status_code=500, detail=f"Error retrieving company info: {str(e)}"
        )
