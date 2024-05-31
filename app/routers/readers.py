# FastAPI
from fastapi import APIRouter, HTTPException, UploadFile, BackgroundTasks

# Pathlib and Enum
from pathlib import Path
from enum import Enum

# Schemas
from app.schemas import FileType, DigestDocsPayload

# Import Digestion Logic
from app.digestion import digest_docs


# Read PDF File
reader = APIRouter(prefix="/knowledgebase")


# Mapping MIME types to the enum
MIME_TYPE_MAPPING = {
    "application/pdf": FileType.PDF,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": FileType.EXCEL,
    "application/vnd.ms-excel": FileType.EXCEL
}


@reader.post("/uploadfile/")
async def create_upload_file(file: UploadFile,
                             background_tasks: BackgroundTasks):
    """
    Simple endpoint to upload files.
    """

    file_type = MIME_TYPE_MAPPING.get(file.content_type)

    # Check for a correct mapping
    if file_type is None:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and Excel files are allowed.")

    # Create a temporary file path
    file_location = f"/tmp/{file.filename}"

    # Convert the file path to Path-like object
    file_path = Path(file_location)

    # Ensure the file exists
    if not file_path.exists():
        raise HTTPException(status_code=500, detail="File could not be saved.")

    # Create payload and add task
    payload = DigestDocsPayload(file_path=file_path, file_type=file_type)

    
    background_tasks.add_task(digest_docs, payload)

    return {"message": "Notification sent in the background"}
