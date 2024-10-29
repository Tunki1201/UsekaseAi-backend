from fastapi import APIRouter, HTTPException
from typing import List
from app.models.prompt_data_model import PromptData
from app.controllers import prompt_data_controller

router = APIRouter()


# GET all prompt data records
@router.get("/prompt-data/", response_model=List[PromptData])
async def get_prompt_data():
    return await prompt_data_controller.get_all_prompt_data()


# GET a specific prompt data record by ID
@router.get("/prompt-data/{id}", response_model=PromptData)
async def get_prompt_data_record(id: str):
    prompt_data = await prompt_data_controller.get_prompt_data_by_id(id)
    if prompt_data is None:
        raise HTTPException(status_code=404, detail="Prompt Data record not found")
    return prompt_data


# POST: Create a new prompt data record
@router.post("/prompt-data/", response_model=PromptData)
async def create_prompt_data(prompt_data: PromptData):
    return await prompt_data_controller.create_prompt_data(prompt_data)


# PUT: Update a prompt data record by ID
@router.put("/prompt-data/{id}", response_model=PromptData)
async def update_prompt_data(id: str, prompt_data: PromptData):
    updated_prompt_data = await prompt_data_controller.update_prompt_data(
        id, prompt_data
    )
    if updated_prompt_data is None:
        raise HTTPException(status_code=404, detail="Prompt Data record not found")
    return updated_prompt_data


# DELETE: Delete a prompt data record by ID
@router.delete("/prompt-data/{id}")
async def delete_prompt_data(id: str):
    deleted = await prompt_data_controller.delete_prompt_data(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Prompt Data record not found")
    return {"status": "Prompt Data record deleted"}
