from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.user_model import User
from app.controllers import user_controller
from app.schema import LoginPayload

router = APIRouter()


# GET all users
@router.get("/get/", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users():
    users = await user_controller.get_all_users()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found."
        )
    return users


# GET a specific user by ID
@router.get("/get/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(user_id: str):
    user = await user_controller.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return user


# POST: Create a new user
@router.post("/create/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: LoginPayload):
    created_user = await user_controller.create_user(user)
    return created_user


# PUT: Update a user by ID
@router.put("/update/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user: LoginPayload):
    updated_user = await user_controller.update_user(user_id, user)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return updated_user


# DELETE: Delete a user by ID
@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    deleted = await user_controller.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return {"detail": "User deleted successfully."}
