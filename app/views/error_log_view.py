from fastapi import APIRouter, HTTPException
from typing import List
from models.error_log_model import ErrorLog
from controllers import error_log_controller

router = APIRouter()


# GET all error logs
@router.get("/error-logs/", response_model=List[ErrorLog])
async def get_error_logs():
    return await error_log_controller.get_all_error_logs()


# GET a specific error log by ID
@router.get("/error-logs/{id}", response_model=ErrorLog)
async def get_error_log(id: str):
    error_log = await error_log_controller.get_error_log_by_id(id)
    if error_log is None:
        raise HTTPException(status_code=404, detail="Error Log not found")
    return error_log


# POST: Create a new error log
@router.post("/error-logs/", response_model=ErrorLog)
async def create_error_log(error_log: ErrorLog):
    return await error_log_controller.create_error_log(error_log)


# PUT: Update an error log by ID
@router.put("/error-logs/{id}", response_model=ErrorLog)
async def update_error_log(id: str, error_log: ErrorLog):
    updated_error_log = await error_log_controller.update_error_log(id, error_log)
    if updated_error_log is None:
        raise HTTPException(status_code=404, detail="Error Log not found")
    return updated_error_log


# DELETE: Delete an error log by ID
@router.delete("/error-logs/{id}")
async def delete_error_log(id: str):
    deleted = await error_log_controller.delete_error_log(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Error Log not found")
    return {"status": "Error Log deleted"}
