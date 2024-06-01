# Queue and Threading
from queue import Queue
from threading import Thread
import asyncio

# FastAPI
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse

# CORS Middleware
from fastapi.middleware.cors import CORSMiddleware

# Asyncronous context manager
from contextlib import asynccontextmanager

# Import routers
from app.routers.readers import file_reader_router

# Import Pubsub manager
from app.events import pubsub_manager



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles resources before app startup (before requests come in) and after shutdown (once requests stop coming in)"""

    # Initialize the S3 Connection
    # S3ClientConnection.initialize()

    yield


# Main Application
app = FastAPI(lifespan=lifespan)

# Store connections
connections = []

@app.get("/events")
async def events():
    queue = asyncio.Queue()

    def callback(event):
        asyncio.create_task(queue.put(event))

    pubsub_manager.subscribe("digest_complete", callback)

    async def event_generator():
        try:
            while True:
                event = await queue.get()
                print("hey")
                yield f"data: {event}\n\n"
        except asyncio.CancelledError:
            pubsub_manager.subscribers["digest_complete"].remove(callback)
            raise

    return StreamingResponse(event_generator(), media_type="text/event-stream")

async def notify_clients(event):
    for connection in connections:
        await connection.put(event)

# Subscribe to the event
pubsub_manager.subscribe("digest_complete", notify_clients)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include Auth Router
app.include_router(file_reader_router)
