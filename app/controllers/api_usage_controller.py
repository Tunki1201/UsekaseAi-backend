from bson import ObjectId
from app.models.api_usage_model import api_usage_collection, api_usage_helper, APIUsage

# CRUD Operations for API Usage


# Get all API usage records
async def get_all_api_usage():
    api_usages = await api_usage_collection.find().to_list(1000)
    return [api_usage_helper(usage) for usage in api_usages]


# Get a specific API usage record by ID
async def get_api_usage_by_id(id: str):
    api_usage = await api_usage_collection.find_one({"_id": ObjectId(id)})
    if api_usage:
        return api_usage_helper(api_usage)
    return None


# Create a new API usage record
async def create_api_usage(api_usage: APIUsage):
    api_usage_dict = api_usage.dict(by_alias=True)
    new_api_usage = await api_usage_collection.insert_one(api_usage_dict)
    created_api_usage = await api_usage_collection.find_one(
        {"_id": new_api_usage.inserted_id}
    )
    return api_usage_helper(created_api_usage)


# Update an existing API usage record by ID
async def update_api_usage(id: str, api_usage_data: APIUsage):
    updated_api_usage = await api_usage_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": api_usage_data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_api_usage:
        return api_usage_helper(updated_api_usage)
    return None


# Delete an API usage record by ID
async def delete_api_usage(id: str):
    result = await api_usage_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
