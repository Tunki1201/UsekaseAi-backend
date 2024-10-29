from fastapi import APIRouter, HTTPException
from typing import List
from app.models.api_usage_model import APIUsage
from app.controllers import api_usage_controller

router = APIRouter()


# GET all API usage records
@router.get("/api-usage/", response_model=List[APIUsage])
async def get_api_usage():
    return await api_usage_controller.get_all_api_usage()


# GET a specific API usage record by ID
@router.get("/api-usage/{id}", response_model=APIUsage)
async def get_api_usage_record(id: str):
    api_usage = await api_usage_controller.get_api_usage_by_id(id)
    if api_usage is None:
        raise HTTPException(status_code=404, detail="API Usage record not found")
    return api_usage


# POST: Create a new API usage record
@router.post("/api-usage/", response_model=APIUsage)
async def create_api_usage(api_usage: APIUsage):
    return await api_usage_controller.create_api_usage(api_usage)


# PUT: Update an API usage record by ID
@router.put("/api-usage/{id}", response_model=APIUsage)
async def update_api_usage(id: str, api_usage: APIUsage):
    updated_api_usage = await api_usage_controller.update_api_usage(id, api_usage)
    if updated_api_usage is None:
        raise HTTPException(status_code=404, detail="API Usage record not found")
    return updated_api_usage


# DELETE: Delete an API usage record by ID
@router.delete("/api-usage/{id}")
async def delete_api_usage(id: str):
    deleted = await api_usage_controller.delete_api_usage(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="API Usage record not found")
    return {"status": "API Usage record deleted"}
