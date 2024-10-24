from fastapi import APIRouter, HTTPException
from typing import List
from models.notification_model import Notification
from controllers import notification_controller

router = APIRouter()


# GET all notifications
@router.get("/notifications/", response_model=List[Notification])
async def get_notifications():
    return await notification_controller.get_all_notifications()


# GET a specific notification by ID
@router.get("/notifications/{id}", response_model=Notification)
async def get_notification(id: str):
    notification = await notification_controller.get_notification_by_id(id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


# POST: Create a new notification
@router.post("/notifications/", response_model=Notification)
async def create_notification(notification: Notification):
    return await notification_controller.create_notification(notification)


# PUT: Update a notification by ID
@router.put("/notifications/{id}", response_model=Notification)
async def update_notification(id: str, notification: Notification):
    updated_notification = await notification_controller.update_notification(
        id, notification
    )
    if updated_notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated_notification


# DELETE: Delete a notification by ID
@router.delete("/notifications/{id}")
async def delete_notification(id: str):
    deleted = await notification_controller.delete_notification(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"status": "Notification deleted"}
