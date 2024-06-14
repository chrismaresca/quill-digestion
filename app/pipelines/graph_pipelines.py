# app/pipelines/graph_pipeline.py

from app.pipelines.pipeline import BasePipeline, PipelineRegistry
from app.clients import Neo4jClient
from app.payloads import FilePayload
import logging

logger = logging.getLogger(__name__)

class GraphPipeline(BasePipeline):
    file_parser: LlamaParse = None
    node_parser: NodeParser = None
    graph_client: Neo4jClient = None

    @classmethod
    def initialize(cls):
        cls.file_parser = LlamaParse()
        cls.node_parser = NodeParser()
        cls.graph_client = Neo4jClient.get_driver()  # Singleton instance
        PipelineRegistry.register_pipeline(cls)  # Register the pipeline

    @classmethod
    def execute(cls, store_namespace: str, files: List[FilePayload], metadata: Dict[str, Any], **kwargs):
        """
        Execute the pipeline to process and index the file.
        
        Args:
            store_namespace (str): The store namespace.
            files (List[FilePayload]): The files to process.
            metadata (Dict[str, Any]): Additional metadata.
            **kwargs: Additional keyword arguments.
        """
        try:
            store = cls.graph_client.get_or_create_store(store_namespace)
            for file in files:
                documents = cls.file_parser.load_data(file_path=file.file_path, extra_info=metadata)
                raw_nodes = cls.node_parser.get_nodes_from_documents(documents=documents)
                nodes_to_index = cls._process_nodes(raw_nodes, file_id=file.file_id, **kwargs)
                store.add(nodes=nodes_to_index)
        except Exception as e:
            logger.error(f"An error occurred during execution: {e}")
