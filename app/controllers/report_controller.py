import os
from typing import Dict, Optional
from urllib.parse import urlparse
from bson import ObjectId
from pydantic import BaseModel, Field
import requests
from app.models.report_model import report_collection, report_helper, Report
from datetime import datetime
from app.utils.report_generator import ReportGenerator
from app.models.scraped_data_model import scraped_data_collection
from pymongo.errors import PyMongoError

# CRUD Operations for Report
# Define the folder to save the downloaded files
BACKEND_REPORTS_FOLDER = os.path.join(os.getcwd(), "backend_reports")

# Ensure the folder exists
os.makedirs(BACKEND_REPORTS_FOLDER, exist_ok=True)


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


def generate_unique_folder_name(url: str, client_id: str) -> str:
    """
    Generate a unique folder name based on the company URL, client ID, and current date.

    :param url: The company URL.
    :param client_id: The client ID.
    :return: The generated unique folder path.
    """
    # Get the domain from the URL to avoid using long URLs directly in the folder name
    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.replace(
        ".", "_"
    )  # Replace dots with underscores for valid folder names

    # Get the current date in YYYYMMDD format
    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a unique folder name using URL domain, client ID, and current date
    folder_name = f"{domain_name}_{client_id}_{current_date}"

    # Ensure the folder is created under the 'backend' folder
    backend_folder = "backend"  # Your desired base folder path
    unique_folder_path = os.path.join(backend_folder, folder_name)

    # Create the folder if it does not exist
    os.makedirs(unique_folder_path, exist_ok=True)

    return unique_folder_path


async def generate_report(url: str, clientId: str) -> dict:
    """
    Fetch company data, check if a report already exists for the given URL and clientId,
    and either return the existing report or generate a new one.

    :param url: The company URL.
    :param clientId: The client ID for the report.
    :return: The generated or existing report data.
    """
    try:
        # Check if a report already exists for this url and clientId
        existing_report = await report_collection.find_one(
            {"company_url": url, "client_id": clientId}
        )

        if existing_report:
            # If a report already exists, return it
            return existing_report.get("chapters", {})

        # If no existing report is found, proceed with generating a new report
        # Fetch the company data from the database
        company_data = await scraped_data_collection.find_one({"company_url": url})
        if not company_data:
            return None  # No company data found, so no report can be generated

        # Use the ReportGenerator to create the report
        report = await ReportGenerator.generate_report(company_data)

        # Generate a unique folder to save downloaded files
        unique_folder_path = generate_unique_folder_name(url, clientId)

        # Download the files from file.io and save them locally
        downloaded_files = {}
        for chapter, file_url in report.items():
            try:
                # Download the file from file.io
                file_data = requests.get(file_url)
                if file_data.status_code == 200:
                    # Extract the file name from the chapter name or use the chapter as the name
                    file_name = (
                        chapter + ".pdf"
                    )  # You can adjust the file extension based on the type
                    file_path = os.path.join(unique_folder_path, file_name)

                    # Save the file locally
                    with open(file_path, "wb") as f:
                        f.write(file_data.content)

                    # Update the report data with the local file path
                    downloaded_files[chapter] = file_path
                else:
                    print(f"Failed to download {chapter} from {file_url}")
                    downloaded_files[chapter] = None
            except Exception as e:
                print(f"Error downloading {chapter} from {file_url}: {e}")
                downloaded_files[chapter] = None

        # Create the new report object
        report_data = {
            "number": "RPT-DEFAULT",  # Or generate a unique identifier if needed
            "chapters": downloaded_files,  # Store the local file paths
            "tone": "neutral",  # Default or set dynamically
            "downloaded": False,  # Initial state
            "created_at": datetime.utcnow(),
            "client_id": clientId,
            "account_id": "UNKNOWN_ACCOUNT",  # Update based on your requirements
            "company_url": url,
        }

        # Insert the new report into the database
        await report_collection.insert_one(report_data)

        # Return the inserted report
        return report_data["chapters"]

    except PyMongoError as e:
        print(f"Database error in generate_report: {str(e)}")
        raise Exception("Database error occurred.")
    except Exception as e:
        print(f"Error in generate_report: {str(e)}")
        raise Exception("An error occurred while generating the report.")
