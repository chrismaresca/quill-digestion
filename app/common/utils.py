import re
import uuid
import uuid
from typing import List, Literal
from pathlib import Path

from app.common.llama import BaseEmbedding, TransformComponent

from app.clients import S3Client




def create_store_namespace(namespace: str, pipeline_type: Literal['vector', 'graph']) -> str:
    """Create a store namespace by combining the namespace and pipeline name."""
    return f"{namespace}:{pipeline_type}"


def id_func(file_id: str) -> str:
    """
    Takes in a file_id and returns it concatenated with a unique UUID4.
    """
    return f"{file_id}#{str(uuid.uuid4())}"


def add_embedding_model(transformations: List[TransformComponent], embed_model: TransformComponent):
    """
    Check if an instance of BaseEmbedding is already in the transformations list.
    """
    if any(isinstance(t, BaseEmbedding) for t in transformations):
        raise ValueError("An instance of BaseEmbedding is already present in the transformations.")
    transformations.append(embed_model)


def clean_filename(filename: str) -> str:
    """
    Clean up the filename by converting it to lowercase and replacing spaces with hyphens.
    """
    cleaned_name = filename.lower()
    cleaned_name = re.sub(r'\s+', '-', cleaned_name)
    return cleaned_name


def read_from_file_service(file_key: str, bucket_name: str = 'workmaitblogimages') -> Path:
    """
    Read a file from S3 and return a Path-like object to access it.

    """
    s3_fs = S3Client.get_filesystem()
    s3_path = f's3://{bucket_name}/{file_key}'

    try:
        # Ensure the file exists by attempting to open it
        with s3_fs.open(s3_path, 'rb') as f:
            pass
    except Exception as e:
        print(f"Failed to access file from S3: {e}")
        raise

    return Path(s3_path)
