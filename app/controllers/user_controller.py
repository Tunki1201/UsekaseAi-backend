from bson import ObjectId
from app.models.user_model import user_collection, user_helper, User
from datetime import datetime

# CRUD Operations


async def get_all_users():
    users = await user_collection.find().to_list(1000)
    return [user_helper(user) for user in users]


async def get_user_by_id(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)
    return None


async def create_user(user: User):
    user_dict = user.dict(by_alias=True)
    user_dict["created_at"] = datetime.utcnow()
    user_dict["modified_at"] = datetime.utcnow()
    new_user = await user_collection.insert_one(user_dict)
    created_user = await user_collection.find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)


async def update_user(id: str, user_data: User):
    updated_user = await user_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": user_data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_user:
        return user_helper(updated_user)
    return None


async def delete_user(id: str):
    result = await user_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
