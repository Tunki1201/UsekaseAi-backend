from bson import ObjectId
from app.models.account_model import account_collection, account_helper, Account

# CRUD Operations for Account


# Get all accounts
async def get_all_accounts():
    accounts = await account_collection.find().to_list(1000)
    return [account_helper(account) for account in accounts]


# Get a specific account by ID
async def get_account_by_id(id: str):
    account = await account_collection.find_one({"_id": ObjectId(id)})
    if account:
        return account_helper(account)
    return None


# Create a new account
async def create_account(account: Account):
    account_dict = account.dict(by_alias=True)
    new_account = await account_collection.insert_one(account_dict)
    created_account = await account_collection.find_one(
        {"_id": new_account.inserted_id}
    )
    return account_helper(created_account)


# Update an existing account by ID
async def update_account(id: str, account_data: Account):
    updated_account = await account_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": account_data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_account:
        return account_helper(updated_account)
    return None


# Delete an account by ID
async def delete_account(id: str):
    result = await account_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
