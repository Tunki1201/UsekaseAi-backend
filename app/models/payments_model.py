from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from database.mongodb import db  # Import the database setup

# MongoDB Payments collection
payments_collection = db["payments"]


# Pydantic model for Payments
class Payment(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    user_id: ObjectId  # Reference to User ID
    amount: float  # Payment amount
    credits_purchased: Optional[int]  # Credits purchased
    payment_status: str  # Status of the payment (e.g., "completed", "pending")
    payment_method: str  # Method of payment (e.g., "credit card", "PayPal")
    created_at: Optional[str] = Field(
        None, alias="created_at"
    )  # Time when the payment was created
    updated_at: Optional[str] = Field(
        None, alias="updated_at"
    )  # Time when the payment was updated

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


# MongoDB to Pydantic conversion helper
def payment_helper(payment) -> dict:
    return {
        "id": str(payment["_id"]),
        "user_id": payment["user_id"],
        "amount": payment["amount"],
        "credits_purchased": payment.get("credits_purchased"),
        "payment_status": payment["payment_status"],
        "payment_method": payment["payment_method"],
        "created_at": payment.get("created_at"),
        "updated_at": payment.get("updated_at"),
    }
