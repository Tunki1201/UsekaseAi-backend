from fastapi import APIRouter, HTTPException
from typing import List
from app.models.scraped_data_model import ScrapedData
from app.controllers import scraped_data_controller

router = APIRouter()


# GET all scraped data
@router.get("/scraped-data/", response_model=List[ScrapedData])
async def get_scraped_data():
    return await scraped_data_controller.get_all_scraped_data()


# GET a specific scraped data entry by ID
@router.get("/scraped-data/{id}", response_model=ScrapedData)
async def get_scraped_data_entry(id: str):
    scraped_data = await scraped_data_controller.get_scraped_data_by_id(id)
    if scraped_data is None:
        raise HTTPException(status_code=404, detail="Scraped data not found")
    return scraped_data


# POST: Create a new scraped data entry
@router.post("/scraped-data/", response_model=ScrapedData)
async def create_scraped_data_entry(data: ScrapedData):
    return await scraped_data_controller.create_scraped_data(data)


# PUT: Update a scraped data entry by ID
@router.put("/scraped-data/{id}", response_model=ScrapedData)
async def update_scraped_data_entry(id: str, data: ScrapedData):
    updated_data = await scraped_data_controller.update_scraped_data(id, data)
    if updated_data is None:
        raise HTTPException(status_code=404, detail="Scraped data not found")
    return updated_data


# DELETE: Delete a scraped data entry by ID
@router.delete("/scraped-data/{id}")
async def delete_scraped_data_entry(id: str):
    deleted = await scraped_data_controller.delete_scraped_data(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Scraped data not found")
    return {"status": "Scraped data deleted"}
