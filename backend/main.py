from fastapi import FastAPI, WebSocket, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pymongo import MongoClient
from passlib.context import CryptContext
import jwt
import os
import asyncio
import logging
from datetime import datetime, timedelta

from dotenv import load_dotenv
from routes import pdfRoutes, searchRoutes, chatRoutes, welcomeRouter

# Load environment variables
load_dotenv()
app = FastAPI(title="RAG System")

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client["rag_db"]
users_collection = db["users"]

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 300

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# WebSocket Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("backend")
clients = set()

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection to send logs in real-time."""
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        clients.remove(websocket)

def send_log(message):
    """Send log messages to WebSocket clients."""
    logger.info(message)
    asyncio.create_task(broadcast_log(message))

async def broadcast_log(message):
    """Broadcast log messages to all active clients."""
    for client in clients:
        try:
            await client.send_text(message)
        except:
            clients.remove(client)

@app.get("/")
def read_root():
    """Root endpoint to check if the API is running."""
    send_log("API is running!")
    return {"message": "Hello, World!"}

@app.get("/process")
def process_something():
    """Example processing function with logging."""
    send_log("Processing started...")
    asyncio.sleep(2)
    send_log("Processing completed.")
    return {"message": "Process Done"}

# Hashing Passwords
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token Generation
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Authentication Routes
@app.post("/auth/register")
async def register(username: str, password: str):
    """User registration endpoint."""
    existing_user = users_collection.find_one({"username": username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_password})

    return {"message": "User registered successfully"}

@app.post("/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint that returns a JWT token."""
    user = users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Fetch the current user details using the JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = users_collection.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return {"username": user["username"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],
)

app.include_router(welcomeRouter.router, prefix="/welcome")
app.include_router(pdfRoutes.router, prefix="/pdf")
app.include_router(searchRoutes.router, prefix="/search")
app.include_router(chatRoutes.router, prefix="/chat")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
