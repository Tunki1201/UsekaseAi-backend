from fastapi import APIRouter, HTTPException
from typing import List
from models.report_model import Report
from controllers import report_controller

router = APIRouter()


# GET all reports
@router.get("/reports/", response_model=List[Report])
async def get_reports():
    return await report_controller.get_all_reports()


# GET a specific report by ID
@router.get("/reports/{id}", response_model=Report)
async def get_report(id: str):
    report = await report_controller.get_report_by_id(id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


# POST: Create a new report
@router.post("/reports/", response_model=Report)
async def create_report(report: Report):
    return await report_controller.create_report(report)


# PUT: Update a report by ID
@router.put("/reports/{id}", response_model=Report)
async def update_report(id: str, report: Report):
    updated_report = await report_controller.update_report(id, report)
    if updated_report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return updated_report


# DELETE: Delete a report by ID
@router.delete("/reports/{id}")
async def delete_report(id: str):
    deleted = await report_controller.delete_report(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "Report deleted"}
