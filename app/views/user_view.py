from fastapi import APIRouter, HTTPException
from typing import List
from app.models.user_model import User
from app.controllers import user_controller

router = APIRouter()


# GET all users
@router.get("/getAll/", response_model=List[User])
async def get_users():
    return await user_controller.get_all_users()


# GET a specific user by ID
@router.get("/getUserById/{id}", response_model=User)
async def get_user(id: str):
    user = await user_controller.get_user_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# POST: Create a new user
@router.post("/create/", response_model=User)
async def create_user(user: User):
    return await user_controller.create_user(user)


# PUT: Update a user by ID
@router.put("/update/{id}", response_model=User)
async def update_user(id: str, user: User):
    updated_user = await user_controller.update_user(id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


# DELETE: Delete a user by ID
@router.delete("/delete/{id}")
async def delete_user(id: str):
    deleted = await user_controller.delete_user(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "User deleted"}
