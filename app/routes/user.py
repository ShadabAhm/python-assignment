from fastapi import APIRouter, HTTPException
from app.models import User
from app.schemas import UserCreate, UserLogin
from app.database import db
from app.auth import hash_password, verify_password

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate):
    user_exists = db.users.find_one({"email": user.email})
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = hash_password(user.password)
    db.users.insert_one({"username": user.username, "email": user.email, "password": hashed_password})
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserLogin):
    db_user = db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}
