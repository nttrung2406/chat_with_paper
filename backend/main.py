from fastapi import FastAPI
from routes import pdfRoutes, searchRoutes, chatRoutes, welcomeRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG System")

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

 
