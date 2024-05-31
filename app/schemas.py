from pydantic import BaseModel, Field

from datetime import datetime
from pathlib import Path
from enum import Enum


class FileType(str, Enum):
    """
    Ensures consistent file type for digestion logic.
    """
    PDF = "PDF"
    EXCEL = "EXCEL"


class DigestDocsPayload(BaseModel):
    """
    Digest Docs Payload
    """
    file_path: Path = Field(description="Path-like representation of the file.")
    file_type: FileType = Field(description="Type of the file.")
    timestamp: datetime = Field(default_factory=datetime.now(datetime.UTC), description="Timestamp when the file was uploaded.")


