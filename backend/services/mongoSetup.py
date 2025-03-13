from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB Atlas
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["chat_with_pdf"]
collection = db["documents"]

document = {
    "text": "Example text",
    "embedding": [0.0] * 512 
}

collection.insert_one(document)

print("MongoDB setup completed!")
