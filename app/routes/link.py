from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import db

router = APIRouter()

class LinkID(BaseModel):
    user_email: str
    id_to_link: str

@router.post("/link_id")
async def link_id(link_id: LinkID):
    user = db.users.find_one({"email": link_id.user_email})
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    db.users.update_one({"email": link_id.user_email}, {"$set": {"linked_id": link_id.id_to_link}})
    return {"message": "ID linked successfully"}
