from fastapi import APIRouter, HTTPException
from typing import List
from models.client_model import Client
from controllers import client_controller

router = APIRouter()


# GET all clients
@router.get("/clients/", response_model=List[Client])
async def get_clients():
    return await client_controller.get_all_clients()


# GET a specific client by ID
@router.get("/clients/{id}", response_model=Client)
async def get_client(id: str):
    client = await client_controller.get_client_by_id(id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


# POST: Create a new client
@router.post("/clients/", response_model=Client)
async def create_client(client: Client):
    return await client_controller.create_client(client)


# PUT: Update a client by ID
@router.put("/clients/{id}", response_model=Client)
async def update_client(id: str, client: Client):
    updated_client = await client_controller.update_client(id, client)
    if updated_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client


# DELETE: Delete a client by ID
@router.delete("/clients/{id}")
async def delete_client(id: str):
    deleted = await client_controller.delete_client(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"status": "Client deleted"}
