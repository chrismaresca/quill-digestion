from pydantic import BaseModel, Field

from datetime import datetime, UTC
from pathlib import Path
from enum import Enum


class FileType(str, Enum):
    """
    Ensures consistent file type for digestion logic.
    """
    PDF = "PDF"
    EXCEL = "EXCEL"


class DigestFilePayload(BaseModel):
    """
    Digest Docs Payload
    """
    file_path: Path = Field(description="Path-like representation of the file.")
    file_type: FileType = Field(description="Type of the file.")
    file_name: str = Field(description="The file name. Not clean.")
    timestamp: datetime = Field(default=datetime.now(UTC), description="Timestamp when the file was uploaded.")


