# Typing Imports
from typing import Union

# llama Index Imports
from llama_parse import LlamaParse
from llama_index.core.node_parser import NodeParser
from llama_index.core.node_parser.relational.base_element import BaseElementNodeParser
from llama_index.core.vector_stores.types import VectorStore, BasePydanticVectorStore
from beanie.odm.fields import PydanticObjectId


# TODO: Fix this
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.base.embeddings.base import BaseEmbedding

# Import Ingestion Pipeline
from app.utils import IDAppender


class DigestionPipeline:
    """
    Pipeline to handle the digestion of files into a vector index.
    """

    def __init__(self, file_id: PydanticObjectId, file_parser: LlamaParse, node_parser: NodeParser, vector_store: Union[VectorStore, BasePydanticVectorStore], embed_model: BaseEmbedding):
        """
        Initialize the pipeline with a file reader, node parser, and vector index manager.
        """
        self.file_id = file_id
        self.file_parser = file_parser
        self.node_parser = node_parser
        self.vector_store = vector_store
        self.embed_model = embed_model

    def execute(self, file_path: str, show_progress: bool = False):
        """
        Execute the digestion of the file.
        """

        try:
            # Load documents using the file reader
            documents = self.file_parser.load_data(file_path)

            # Parse nodes from the documents
            raw_nodes = self.node_parser.get_nodes_from_documents(documents=documents, show_progress=show_progress)

            # Get the nodes to index
            nodes_to_index = self._process_nodes(raw_nodes)

            # Add nodes to the vector index
            index_ids = self.vector_store.add(nodes=nodes_to_index)

            return index_ids

        except Exception as e:
            # Handle exceptions and log errors
            print(f"An error occurred during execution: {e}")

    def _process_nodes(self, raw_nodes):
        """
        Process raw nodes based on the parser type.
        """

        try:
            node_pipeline = self._create_node_pipeline()
            embedded_nodes = node_pipeline.run(nodes=raw_nodes)

            if isinstance(self.node_parser, BaseElementNodeParser):
                # Get the text nodes and tables if the parser is capable of identifying both
                base_nodes, object_nodes = self.node_parser.get_nodes_and_objects(embedded_nodes)
                return base_nodes + object_nodes
            else:
                return embedded_nodes
        except Exception as e:
            print(f"An error occurred while processing nodes: {e}")
            return []

    def _create_node_pipeline(self):
        """
        Create an ingestion pipeline with the embedding model.
        """
        return IngestionPipeline(transformations=[self.embed_model, IDAppender()])
