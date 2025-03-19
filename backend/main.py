from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from routes import pdfRoutes, searchRoutes, chatRoutes, welcomeRouter, registerRoutes, loginRoutes

load_dotenv()
app = FastAPI(title="RAG System")

client = MongoClient(os.getenv("MONGO_URI"))
db = client["rag_db"]
users_collection = db["users"]


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
app.include_router(registerRoutes.router)
app.include_router(loginRoutes.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
