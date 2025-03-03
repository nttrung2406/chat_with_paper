from fastapi import FastAPI
from routes import pdfRoutes, searchRoutes, chatRoutes

app = FastAPI(title="RAG System with LLaVA and Milvus")

# Include routes
app.include_router(pdfRoutes.router, prefix="/pdf", tags=["PDF Processing"])
app.include_router(searchRoutes.router, prefix="/search", tags=["Search"])
app.include_router(chatRoutes.router, prefix="/chat", tags=["Chat"])

@app.get("/")
def home():
    return {"message": "Welcome to LLaVA-powered RAG Chatbot!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)