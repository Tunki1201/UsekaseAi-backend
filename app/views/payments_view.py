from fastapi import APIRouter, HTTPException
from typing import List
from app.models.payments_model import Payment
from app.controllers import payments_controller

router = APIRouter()


# GET all payments
@router.get("/payments/", response_model=List[Payment])
async def get_payments():
    return await payments_controller.get_all_payments()


# GET a specific payment by ID
@router.get("/payments/{id}", response_model=Payment)
async def get_payment(id: str):
    payment = await payments_controller.get_payment_by_id(id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


# POST: Create a new payment
@router.post("/payments/", response_model=Payment)
async def create_payment(payment: Payment):
    return await payments_controller.create_payment(payment)


# PUT: Update a payment by ID
@router.put("/payments/{id}", response_model=Payment)
async def update_payment(id: str, payment: Payment):
    updated_payment = await payments_controller.update_payment(id, payment)
    if updated_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment


# DELETE: Delete a payment by ID
@router.delete("/payments/{id}")
async def delete_payment(id: str):
    deleted = await payments_controller.delete_payment(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"status": "Payment deleted"}
