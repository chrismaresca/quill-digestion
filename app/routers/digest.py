# Typing
from typing import Annotated

# Asyncio
import asyncio

# FastAPI
from fastapi import APIRouter, HTTPException, UploadFile, BackgroundTasks, Depends
from fastapi.responses import StreamingResponse

# Pathlib and Enum
from pathlib import Path
from enum import Enum

# Schemas
from app.schemas import FileType, DigestFilePayload

# Import Digestion Logic
from app.services import digest_file

# Import Pubsub manager
from app.events import pubsub_manager

# Dependencies
from app.dependencies import get_digestion_clients


# Read PDF File
digest_router = APIRouter(prefix="/digest", tags=['Digestion'])

# Mapping MIME types to the enum
MIME_TYPE_MAPPING = {
    "application/pdf": FileType.PDF,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": FileType.EXCEL,
    "application/vnd.ms-excel": FileType.EXCEL
}

# Client Dependencies
Clients = Annotated[tuple, Depends(get_digestion_clients)]


@digest_router.post("/digest-file/")
async def digest_file_endpoint(file: UploadFile,
                               background_tasks: BackgroundTasks,
                               clients: Clients):
    """
    Simple endpoint to upload files.
    """

    file_type = MIME_TYPE_MAPPING.get(file.content_type)

    # Check for a correct mapping
    if file_type is None:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and Excel files are allowed.")

    # Create a temporary file path
    tmp_dir = Path("/tmp")
    tmp_dir.mkdir(parents=True, exist_ok=True)  # Ensure the /tmp directory exists
    file_location = tmp_dir / file.filename

    # Save the file to the /tmp directory
    try:
        with file_location.open("wb") as f:
            f.write(await file.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File could not be saved: {str(e)}")

    # Ensure the file exists
    if not file_location.exists():
        raise HTTPException(status_code=500, detail="File could not be saved.")

    # Create payload and add task
    payload = DigestFilePayload(file_path=file_location, file_type=file_type, file_name=file.filename)
    vector_client, llm, embed_model = clients
    background_tasks.add_task(digest_file, payload, vector_client, llm, embed_model)


# Store connections
connections = []


@digest_router.get("/digestion-complete")
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
