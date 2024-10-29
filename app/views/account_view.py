from fastapi import APIRouter, HTTPException
from typing import List
from app.models.account_model import Account
from app.controllers import account_controller

router = APIRouter()


# GET all accounts
@router.get("/accounts/", response_model=List[Account])
async def get_accounts():
    return await account_controller.get_all_accounts()


# GET a specific account by ID
@router.get("/accounts/{id}", response_model=Account)
async def get_account(id: str):
    account = await account_controller.get_account_by_id(id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


# POST: Create a new account
@router.post("/accounts/", response_model=Account)
async def create_account(account: Account):
    return await account_controller.create_account(account)


# PUT: Update an account by ID
@router.put("/accounts/{id}", response_model=Account)
async def update_account(id: str, account: Account):
    updated_account = await account_controller.update_account(id, account)
    if updated_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return updated_account


# DELETE: Delete an account by ID
@router.delete("/accounts/{id}")
async def delete_account(id: str):
    deleted = await account_controller.delete_account(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"status": "Account deleted"}
