from bson import ObjectId
from app.models.chapter_model import chapter_collection, chapter_helper, Chapter

# CRUD Operations for Chapter


# Get all chapters
async def get_all_chapters():
    chapters = await chapter_collection.find().to_list(1000)
    return [chapter_helper(ch) for ch in chapters]


# Get a specific chapter by ID
async def get_chapter_by_id(id: str):
    chapter = await chapter_collection.find_one({"_id": ObjectId(id)})
    if chapter:
        return chapter_helper(chapter)
    return None


# Create a new chapter
async def create_chapter(chapter: Chapter):
    chapter_dict = chapter.dict(by_alias=True)
    new_chapter = await chapter_collection.insert_one(chapter_dict)
    created_chapter = await chapter_collection.find_one(
        {"_id": new_chapter.inserted_id}
    )
    return chapter_helper(created_chapter)


# Update an existing chapter by ID
async def update_chapter(id: str, chapter: Chapter):
    updated_chapter = await chapter_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": chapter.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_chapter:
        return chapter_helper(updated_chapter)
    return None


# Delete a chapter by ID
async def delete_chapter(id: str):
    result = await chapter_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
