from bson import ObjectId
from app.models.error_log_model import error_log_collection, error_log_helper, ErrorLog

# CRUD Operations for Error Log


# Get all error logs
async def get_all_error_logs():
    error_logs = await error_log_collection.find().to_list(1000)
    return [error_log_helper(log) for log in error_logs]


# Get a specific error log by ID
async def get_error_log_by_id(id: str):
    error_log = await error_log_collection.find_one({"_id": ObjectId(id)})
    if error_log:
        return error_log_helper(error_log)
    return None


# Create a new error log
async def create_error_log(error_log: ErrorLog):
    error_log_dict = error_log.dict(by_alias=True)
    new_error_log = await error_log_collection.insert_one(error_log_dict)
    created_error_log = await error_log_collection.find_one(
        {"_id": new_error_log.inserted_id}
    )
    return error_log_helper(created_error_log)


# Update an existing error log by ID
async def update_error_log(id: str, error_log_data: ErrorLog):
    updated_error_log = await error_log_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": error_log_data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_error_log:
        return error_log_helper(updated_error_log)
    return None


# Delete an error log by ID
async def delete_error_log(id: str):
    result = await error_log_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
