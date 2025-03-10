from fastapi import FastAPI, WebSocket
from routes import pdfRoutes, searchRoutes, chatRoutes, welcomeRouter
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging

app = FastAPI(title="RAG System")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("backend")
clients = set()

@app.websocket("/ws/logs")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            await asyncio.sleep(1)
    except:
        clients.remove(websocket)


def send_log(message):
    logger.info(message)
    asyncio.create_task(broadcast_log(message))

async def broadcast_log(message):
    for client in clients:
        try:
            await client.send_text(message)
        except:
            clients.remove(client)

@app.get("/")
def read_root():
    send_log("API is running!")
    return {"message": "Hello, World!"}

@app.get("/process")
def process_something():
    send_log("Processing started...")
    asyncio.sleep(2)
    send_log("Processing completed.")
    return {"message": "Process Done"}

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