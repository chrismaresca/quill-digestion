# app/payloads.py

from pydantic import BaseModel
from typing import List, Dict, Any
from enum import Enum


class FileType(str, Enum):
    PDF = "pdf"
    EXCEL = "excel"
    DOC = "doc"
    PPT = "ppt"


class FilePayload(BaseModel):
    file_id: str
    file_type: FileType
    file_path: str
    file_metadata: Dict[str, Any]


class AddNodesPayload(BaseModel):
    namespace: str
    strategies: List[str]
    files: List[FilePayload]
    payload_metadata: Dict[str, Any]


class DeleteNodesPayload(BaseModel):
    namespace: str
    file_ids: List[str]


class DeleteStorePayload(BaseModel):
    namespace: str


class MoveNodesPayload(BaseModel):
    source_namespace: str
    target_namespace: str
    file_ids: List[str]
