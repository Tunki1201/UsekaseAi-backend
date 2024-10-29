from bson import ObjectId
from app.models.prompt_data_model import (
    prompt_data_collection,
    prompt_data_helper,
    PromptData,
)

# CRUD Operations for Prompt Data


# Get all prompt data records
async def get_all_prompt_data():
    prompt_data_list = await prompt_data_collection.find().to_list(1000)
    return [prompt_data_helper(data) for data in prompt_data_list]


# Get a specific prompt data record by ID
async def get_prompt_data_by_id(id: str):
    prompt_data = await prompt_data_collection.find_one({"_id": ObjectId(id)})
    if prompt_data:
        return prompt_data_helper(prompt_data)
    return None


# Create a new prompt data record
async def create_prompt_data(prompt_data: PromptData):
    prompt_data_dict = prompt_data.dict(by_alias=True)
    new_prompt_data = await prompt_data_collection.insert_one(prompt_data_dict)
    created_prompt_data = await prompt_data_collection.find_one(
        {"_id": new_prompt_data.inserted_id}
    )
    return prompt_data_helper(created_prompt_data)


# Update an existing prompt data record by ID
async def update_prompt_data(id: str, prompt_data: PromptData):
    updated_prompt_data = await prompt_data_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": prompt_data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_prompt_data:
        return prompt_data_helper(updated_prompt_data)
    return None


# Delete a prompt data record by ID
async def delete_prompt_data(id: str):
    result = await prompt_data_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
