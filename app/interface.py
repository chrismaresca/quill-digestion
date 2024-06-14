# app/interface.py

from typing import List, Dict, Literal

# Payloads
from app.payloads import AddNodesPayload, DeleteNodesPayload, DeleteStorePayload, MoveNodesPayload
from app.pipelines import BasePipeline

# Utils
from app.common.utils import create_store_namespace


async def add_nodes(payload: AddNodesPayload):
    """Add nodes to the specified pipeline and store namespace."""
    for strategy_name in payload.strategies:

        pipeline = BasePipeline.get_pipeline(strategy_name=strategy_name)
        store_namespace = create_store_namespace(payload.namespace, pipeline_type=pipeline.pipeline_type)

        await pipeline.execute(store_namespace=store_namespace,
                               file_payloads=payload.files,
                               payload_metadata=payload.payload_metadata,
                               )


async def delete_nodes(payload: DeleteNodesPayload):
    """Delete nodes from the specified namespace."""
    # Implement the logic to delete nodes
    pass


async def delete_store(payload: DeleteStorePayload):
    """Delete the specified store."""
    # Implement the logic to delete store
    pass


async def move_nodes(payload: MoveNodesPayload):
    """Move nodes from the source namespace to the target namespace."""
    # Implement the logic to move nodes
    pass
