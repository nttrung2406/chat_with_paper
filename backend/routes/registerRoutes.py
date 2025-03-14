from fastapi import HTTPException, APIRouter
from services.mongoSetupForUser import users_collection
from models.userModel import User
from utils.helper import hash_password

router = APIRouter()

@router.post("/signup")
async def register_user(user: User):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    user_data = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password
    }
    result = users_collection.insert_one(user_data)
    return {"id": str(result.inserted_id), "message": "User registered successfully"}
