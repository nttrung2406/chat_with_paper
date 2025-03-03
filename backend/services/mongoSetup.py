from pymongo import MongoClient

client = MongoClient("mongodb+srv://admin:admin@cluster0.ooufc.mongodb.net/")
db = client["chat_with_pdf"]
collection = db["documents"]

document = {
    "text": "Example text",
    "embedding": [0.0] * 512 
}

collection.insert_one(document)

print("MongoDB setup completed!")
