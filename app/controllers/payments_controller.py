from bson import ObjectId
from models.payments_model import payments_collection, payment_helper, Payment

# CRUD Operations for Payments


# Get all payments
async def get_all_payments():
    payments = await payments_collection.find().to_list(1000)
    return [payment_helper(payment) for payment in payments]


# Get a specific payment by ID
async def get_payment_by_id(id: str):
    payment = await payments_collection.find_one({"_id": ObjectId(id)})
    if payment:
        return payment_helper(payment)
    return None


# Create a new payment
async def create_payment(payment: Payment):
    payment_dict = payment.dict(by_alias=True)
    new_payment = await payments_collection.insert_one(payment_dict)
    created_payment = await payments_collection.find_one(
        {"_id": new_payment.inserted_id}
    )
    return payment_helper(created_payment)


# Update an existing payment by ID
async def update_payment(id: str, payment_data: Payment):
    updated_payment = await payments_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": payment_data.dict(exclude_unset=True)},
        return_document=True,
    )
    if updated_payment:
        return payment_helper(updated_payment)
    return None


# Delete a payment by ID
async def delete_payment(id: str):
    result = await payments_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
