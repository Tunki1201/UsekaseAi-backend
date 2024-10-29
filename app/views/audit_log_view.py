from fastapi import APIRouter, HTTPException
from typing import List
from app.models.audit_log_model import AuditLog
from app.controllers import audit_log_controller

router = APIRouter()


# GET all audit logs
@router.get("/audit-logs/", response_model=List[AuditLog])
async def get_audit_logs():
    return await audit_log_controller.get_all_audit_logs()


# GET a specific audit log by ID
@router.get("/audit-logs/{id}", response_model=AuditLog)
async def get_audit_log(id: str):
    audit_log = await audit_log_controller.get_audit_log_by_id(id)
    if audit_log is None:
        raise HTTPException(status_code=404, detail="Audit Log not found")
    return audit_log


# POST: Create a new audit log
@router.post("/audit-logs/", response_model=AuditLog)
async def create_audit_log(audit_log: AuditLog):
    return await audit_log_controller.create_audit_log(audit_log)


# PUT: Update an audit log by ID
@router.put("/audit-logs/{id}", response_model=AuditLog)
async def update_audit_log(id: str, audit_log: AuditLog):
    updated_audit_log = await audit_log_controller.update_audit_log(id, audit_log)
    if updated_audit_log is None:
        raise HTTPException(status_code=404, detail="Audit Log not found")
    return updated_audit_log


# DELETE: Delete an audit log by ID
@router.delete("/audit-logs/{id}")
async def delete_audit_log(id: str):
    deleted = await audit_log_controller.delete_audit_log(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Audit Log not found")
    return {"status": "Audit Log deleted"}
