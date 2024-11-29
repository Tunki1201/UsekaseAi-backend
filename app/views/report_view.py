from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models.report_model import Report
from app.controllers import report_controller

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


@router.get("/generate-report/")
async def generate_report_view(
    url: str = Query(..., description="Company URL for report generation"),
    clientId: str = Query(..., description="Client ID for the report"),
):
    """
    Endpoint to generate a report for the provided company URL.
    """
    try:
        # Call the controller to handle the report generation
        report_data = await report_controller.generate_report(url, clientId)

        if not report_data:
            raise HTTPException(
                status_code=404,
                detail="Report generation failed. No data found for the given URL.",
            )

        return {
            "success": True,
            "message": "Report generated successfully.",
            "report_data": report_data,
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        print(f"Error generating report for URL {url}: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Internal server error while generating report."
        )
