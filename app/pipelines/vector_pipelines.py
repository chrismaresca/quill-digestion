# app/pipelines/vector_pipeline.py

from typing import List, Dict, Any, Optional
from pathlib import Path
import logging


from app.pipelines.pipeline import BasePipeline
from app.clients import PineconeClient, BaseAIClient, OpenAIClient, S3Client, RemoteFileServiceClient
from app.payloads import FilePayload

from app.common.llama import (LlamaParse,
                              NodeParser,
                              BaseReader,
                              BaseElementNodeParser,
                              MarkdownElementNodeParser,
                              TransformComponent,
                              IngestionPipeline)

from app.config import workmait_config
from app.common.utils import read_from_file_service, id_func, add_embedding_model
from app.common import exceptions

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------- #


class VectorPipeline(BasePipeline):
    def __init__(self,
                 strategy_name: str,
                 file_parser: BaseReader,
                 node_parser: NodeParser,
                 ai_client: BaseAIClient,
                 transformations: List[TransformComponent],
                 store_client: Optional[PineconeClient] = None,
                 ):
        """
        Initialize the Vector Pipeline.
        """
        super().__init__(strategy_name, 'vector')

        self.file_parser = file_parser
        self.node_parser = node_parser
        self.embed_model = ai_client.embedding
        self.store_client = store_client or PineconeClient.get_index()
        self.transformations = list(set(transformations))

    @classmethod
    def create_pipeline(cls,
                        strategy_name: str,
                        ai_client: BaseAIClient,
                        file_parser: BaseReader,
                        node_parser: NodeParser,
                        transformations: List[TransformComponent],
                        store_client: Optional[PineconeClient] = None,
                        ) -> 'VectorPipeline':
        """
        Build the pipeline.
        """
        embed_model = ai_client.embedding
        # Ensure unique transformations by converting to a set and back to a list
        add_embedding_model(transformations, embed_model)
        instance = cls(strategy_name, file_parser, node_parser, ai_client, transformations, store_client)
        cls.register_pipeline(strategy_name, instance)
        return instance

    def execute(self, store_namespace: str, file_payloads: List[FilePayload], payload_metadata: Dict[str, Any] = None, **kwargs) -> List[str]:
        """Execute the pipeline."""
        index_ids = []
        try:
            store = self.store_client.get_or_create_store(store_namespace)
        except Exception as e:
            logger.error(f"Error getting or creating store for namespace '{store_namespace}': {e}")
            raise exceptions.StoreException(f"StoreCreationException: Error getting or creating store for namespace '{store_namespace}': {e}")

        for file_payload in file_payloads:
            try:
                full_metadata = self._create_file_metadata(file_payload, payload_metadata)
                self.read_from_file_service(file_payload.file_path)
                documents = self._load_data(file_payload.file_path, full_metadata)
                raw_nodes = self._get_nodes_from_documents(file_id=file_payload.file_id, documents=documents)
                nodes_to_index = self._ingest_nodes(raw_nodes, file_payload.file_id, **kwargs)
                index_ids.extend(self._add_nodes_to_store(store, nodes_to_index, file_payload.file_path))
            except exceptions.PipelineStepException as e:
                logger.error(f"Execution error for file '{file_payload.file_path}': {e}")
                continue

        return index_ids

    def _create_file_metadata(self, file_payload: FilePayload, payload_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create full metadata from payload and file metadata."""
        try:
            full_metadata = payload_metadata or {}
            full_metadata.update(file_payload.file_metadata or {})
            return full_metadata
        except Exception as e:
            logger.error(f"Error creating file metadata for file '{file_payload.file_path}': {e}")
            raise exceptions.MetadataCreationException(f"MetadataCreationException: Error creating file metadata for file '{file_payload.file_path}': {e}")

    def _read_from_file_service(self, file_path: str):
        """Read from file service (placeholder implementation)."""
        try:
            read_from_file_service(file_path)
        except Exception as e:
            logger.error(f"Error reading from file service for file '{file_path}': {e}")
            raise exceptions.FileServiceException(f"FileServiceException: Error reading from file service for file '{file_path}': {e}")

    def _load_data(self, file_path: str, full_metadata: Dict[str, Any]):
        """Load data from file."""
        try:
            return self.file_parser.load_data(file_path=file_path, extra_info=full_metadata)
        except Exception as e:
            logger.error(f"Error loading data from file '{file_path}': {e}")
            raise exceptions.FileLoadingException(f"FileLoadingException: Error loading data from file '{file_path}': {e}")

    def _get_nodes_from_documents(self, file_id: str, documents: List):
        """Get nodes from documents."""
        try:
            return self.node_parser.get_nodes_from_documents(documents=documents, id_func=id_func(file_id=file_id))
        except Exception as e:
            logger.error(f"Error getting nodes from documents: {e}")
            raise exceptions.NodeParsingException(f"NodeParsingException: Error getting nodes from documents: {e}")

    def _ingest_nodes(self, raw_nodes, file_id: str, **kwargs):
        """Process raw nodes."""
        try:
            node_pipeline = self._create_node_pipeline(file_id=file_id, **kwargs)
            embedded_nodes = node_pipeline.run(nodes=raw_nodes)
            if isinstance(self.node_parser, BaseElementNodeParser):
                base_nodes, object_nodes = self.node_parser.get_nodes_and_objects(embedded_nodes)
                return base_nodes + object_nodes
            return embedded_nodes
        except Exception as e:
            logger.error(f"Node processing error: {e}")
            raise exceptions.NodeIngestionException(f"NodeIngestionException: Node processing error: {e}")

    def _add_nodes_to_store(self, store, nodes_to_index, file_path: str):
        """Add nodes to store."""
        try:
            return store.add(nodes=nodes_to_index)
        except Exception as e:
            logger.error(f"Error adding nodes to store for file '{file_path}': {e}")
            raise exceptions.StoreAdditionException(f"StoreAdditionException: Error adding nodes to store for file '{file_path}': {e}")

    def _create_node_pipeline(self, **kwargs):
        """Create an ingestion pipeline."""
        transformations = list(set(self.transformations))

        return IngestionPipeline(transformations=transformations)
