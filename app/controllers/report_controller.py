from bson import ObjectId
from app.models.report_model import report_collection, report_helper, Report
from datetime import datetime
from app.utils.report_generator import ReportGenerator
from app.models.scraped_data_model import scraped_data_collection

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


async def generate_report(url: str) -> dict:
    """
    Fetch company data and use the ReportGenerator to create a report.

    :param url: The company URL.
    :return: The generated report.
    """
    try:
        # Fetch the company data from the database
        company_data = await scraped_data_collection.find_one({"company_url": url})
        if not company_data:
            return None

        # Use the ReportGenerator to create the report
        report = await ReportGenerator.generate_report(company_data)

        # # Optionally save the report in the database
        await report_collection.insert_one(report)

        return report

    except Exception as e:
        print(f"Error in generate_report: {str(e)}")
        raise
