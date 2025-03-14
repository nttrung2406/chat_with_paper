from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from dotenv import load_dotenv
from datetime import timedelta
from services.mongoSetupForUser import users_collection
from utils.helper import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
import logging
load_dotenv()

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})
    print("User: %s" % user)
    if not user:
        logging.error(f"User not found: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not verify_password(form_data.password, user["password"]):
        logging.error(f"Incorrect password for user: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
     
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

print("loginRoutes.py loaded!")