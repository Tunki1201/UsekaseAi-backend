from bson import ObjectId
from models.audit_log_model import audit_log_collection, audit_log_helper, AuditLog

# CRUD Operations for Audit Log


# Get all audit logs
async def get_all_audit_logs():
    audit_logs = await audit_log_collection.find().to_list(1000)
    return [audit_log_helper(log) for log in audit_logs]


# Get a specific audit log by ID
async def get_audit_log_by_id(id: str):
    audit_log = await audit_log_collection.find_one({"_id": ObjectId(id)})
    if audit_log:
        return audit_log_helper(audit_log)
    return None


# Create a new audit log
async def create_audit_log(audit_log: AuditLog):
    audit_log_dict = audit_log.dict(by_alias=True)
    new_audit_log = await audit_log_collection.insert_one(audit_log_dict)
    created_audit_log = await audit_log_collection.find_one(
        {"_id": new_audit_log.inserted_id}
    )
    return audit_log_helper(created_audit_log)


# Update an existing audit log by ID
async def update_audit_log(id: str, audit_log_data: AuditLog):
    updated_audit_log = await audit_log_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": audit_log_data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_audit_log:
        return audit_log_helper(updated_audit_log)
    return None


# Delete an audit log by ID
async def delete_audit_log(id: str):
    result = await audit_log_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
