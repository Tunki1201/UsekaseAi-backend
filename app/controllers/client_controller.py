from bson import ObjectId
from models.client_model import client_collection, client_helper, Client

# CRUD Operations for Client


# Get all clients
async def get_all_clients():
    clients = await client_collection.find().to_list(1000)
    return [client_helper(client) for client in clients]


# Get a specific client by ID
async def get_client_by_id(id: str):
    client = await client_collection.find_one({"_id": ObjectId(id)})
    if client:
        return client_helper(client)
    return None


# Create a new client
async def create_client(client: Client):
    client_dict = client.dict(by_alias=True)
    new_client = await client_collection.insert_one(client_dict)
    created_client = await client_collection.find_one({"_id": new_client.inserted_id})
    return client_helper(created_client)


# Update an existing client by ID
async def update_client(id: str, client_data: Client):
    updated_client = await client_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": client_data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_client:
        return client_helper(updated_client)
    return None


# Delete a client by ID
async def delete_client(id: str):
    result = await client_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
