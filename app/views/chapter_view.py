from fastapi import APIRouter, HTTPException
from typing import List
from app.models.chapter_model import Chapter
from app.controllers import chapter_controller

router = APIRouter()


# GET all chapters
@router.get("/chapters/", response_model=List[Chapter])
async def get_chapters():
    return await chapter_controller.get_all_chapters()


# GET a specific chapter by ID
@router.get("/chapters/{id}", response_model=Chapter)
async def get_chapter(id: str):
    chapter = await chapter_controller.get_chapter_by_id(id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


# POST: Create a new chapter
@router.post("/chapters/", response_model=Chapter)
async def create_chapter(chapter: Chapter):
    return await chapter_controller.create_chapter(chapter)


# PUT: Update a chapter by ID
@router.put("/chapters/{id}", response_model=Chapter)
async def update_chapter(id: str, chapter: Chapter):
    updated_chapter = await chapter_controller.update_chapter(id, chapter)
    if updated_chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return updated_chapter


# DELETE: Delete a chapter by ID
@router.delete("/chapters/{id}")
async def delete_chapter(id: str):
    deleted = await chapter_controller.delete_chapter(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return {"status": "Chapter deleted"}
