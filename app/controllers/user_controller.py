from bson import ObjectId
from pymongo.errors import PyMongoError
from datetime import datetime
from typing import Optional, List
from app.models.user_model import User, user_collection, user_helper
from fastapi import HTTPException, status

# CRUD Operations


async def get_all_users() -> List[User]:
    try:
        users = await user_collection.find().to_list(1000)
        return [user_helper(user) for user in users]
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving users.",
        ) from e


async def get_user_by_id(user_id: str) -> Optional[User]:
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format."
        )
    try:
        user = await user_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return user_helper(user)
        return None
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user.",
        ) from e


async def create_user(user: User) -> User:
    # Convert Pydantic model to dict and handle datetime serialization
    user_dict = user.dict(by_alias=True, exclude_unset=True)

    # Validate if the user already exists based on email
    existing_user = await user_collection.find_one({"email": user_dict["email"]})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )

    # Update timestamps
    current_time = datetime.utcnow()
    user_dict["created_at"] = current_time
    user_dict["modified_at"] = current_time

    # Set default values if not provided
    user_dict.setdefault("is_authenticated", True)
    user_dict.setdefault("role", None)
    user_dict.setdefault("team", None)
    user_dict.setdefault("credits_purchased", 0)

    try:
        # Insert the new user into the collection
        new_user = await user_collection.insert_one(user_dict)
        created_user = await user_collection.find_one({"_id": new_user.inserted_id})

        if created_user:
            return user_helper(created_user)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user.",
        )
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}",
        ) from e


async def update_user(user_id: str, user_data: User) -> Optional[User]:
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format."
        )
    user_data.modified_at = datetime.utcnow()
    try:
        updated_user = await user_collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": user_data.dict(exclude_unset=True)},
            return_document=True,
        )
        if updated_user:
            return user_helper(updated_user)
        return None
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating user.",
        ) from e


async def delete_user(user_id: str) -> bool:
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format."
        )
    try:
        result = await user_collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except PyMongoError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting user.",
        ) from e
