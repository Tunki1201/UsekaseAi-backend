from bson import ObjectId
from models.report_model import report_collection, report_helper, Report
from datetime import datetime

# CRUD Operations for Report


# Get all reports
async def get_all_reports():
    reports = await report_collection.find().to_list(1000)
    return [report_helper(report) for report in reports]


# Get a specific report by ID
async def get_report_by_id(id: str):
    report = await report_collection.find_one({"_id": ObjectId(id)})
    if report:
        return report_helper(report)
    return None


# Create a new report
async def create_report(report: Report):
    report_dict = report.dict(by_alias=True)
    report_dict["created_at"] = datetime.utcnow()
    new_report = await report_collection.insert_one(report_dict)
    created_report = await report_collection.find_one({"_id": new_report.inserted_id})
    return report_helper(created_report)


# Update an existing report by ID
async def update_report(id: str, report_data: Report):
    updated_report = await report_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": report_data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_report:
        return report_helper(updated_report)
    return None


# Delete a report by ID
async def delete_report(id: str):
    result = await report_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
