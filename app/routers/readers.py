# FastAPI
from fastapi import APIRouter, HTTPException, UploadFile, BackgroundTasks

# Pathlib and Enum
from pathlib import Path
from enum import Enum

# Schemas
from app.schemas import FileType, DigestFilePayload

# Import Digestion Logic
from app.services import digest_file



# Read PDF File
file_reader_router = APIRouter(prefix="/digest")


# Mapping MIME types to the enum
MIME_TYPE_MAPPING = {
    "application/pdf": FileType.PDF,
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": FileType.EXCEL,
    "application/vnd.ms-excel": FileType.EXCEL
}


@file_reader_router.post("/uploadfile/")
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
    background_tasks.add_task(digest_file, payload)