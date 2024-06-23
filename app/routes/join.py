from fastapi import APIRouter, HTTPException
from app.database import db

router = APIRouter()

@router.get("/join")
async def join_data():
    users = list(db.users.find({}))
    # Example join operation, adjust based on your collections and requirements
    for user in users:
        user_data = db.another_collection.find_one({"user_id": user["_id"]})
        user["extra_data"] = user_data
    return users

@router.delete("/delete_user/{user_email}")
async def delete_user(user_email: str):
    user = db.users.find_one({"email": user_email})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    db.users.delete_one({"email": user_email})
    db.another_collection.delete_many({"user_id": user["_id"]})
    return {"message": "User and associated data deleted successfully"}
