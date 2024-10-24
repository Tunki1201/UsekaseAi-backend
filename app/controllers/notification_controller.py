from bson import ObjectId
from models.notification_model import (
    notification_collection,
    notification_helper,
    Notification,
)

# CRUD Operations for Notifications


# Get all notifications
async def get_all_notifications():
    notifications = await notification_collection.find().to_list(1000)
    return [notification_helper(note) for note in notifications]


# Get a specific notification by ID
async def get_notification_by_id(id: str):
    notification = await notification_collection.find_one({"_id": ObjectId(id)})
    if notification:
        return notification_helper(notification)
    return None


# Create a new notification
async def create_notification(notification: Notification):
    notification_dict = notification.dict(by_alias=True)
    new_notification = await notification_collection.insert_one(notification_dict)
    created_notification = await notification_collection.find_one(
        {"_id": new_notification.inserted_id}
    )
    return notification_helper(created_notification)


# Update an existing notification by ID
async def update_notification(id: str, notification_data: Notification):
    updated_notification = await notification_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": notification_data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_notification:
        return notification_helper(updated_notification)
    return None


# Delete a notification by ID
async def delete_notification(id: str):
    result = await notification_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
