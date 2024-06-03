import re
import uuid
from typing import Optional

from llama_index.core.schema import TransformComponent
from llama_index.core.schema import BaseNode



def clean_filename(filename: str) -> str:
    """
    Clean up the filename by converting it to lowercase and replacing spaces with hyphens.
    """
    cleaned_name = filename.lower()
    cleaned_name = re.sub(r'\s+', '-', cleaned_name)
    return cleaned_name


class IDAppender(TransformComponent):
    def __init__(self):
        self.parent_id = str(uuid.uuid4())

    def __call__(self, nodes, **kwargs):
        for node in nodes:
            node_id = str(uuid.uuid4())
            node.id_ = f"{self.parent_id}:{node_id}"
        return nodes