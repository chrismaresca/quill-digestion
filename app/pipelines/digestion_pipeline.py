# Typing Imports
from typing import Union

# llama Index Imports
from llama_parse import LlamaParse
from llama_index.core.node_parser import NodeParser
from llama_index.core.node_parser.relational.base_element import BaseElementNodeParser
from llama_index.core.vector_stores.types import VectorStore, BasePydanticVectorStore



class DigestionPipeline:
    """
    Pipeline to handle the digestion of files into a vector index.
    """

    def __init__(self, file_parser: LlamaParse, node_parser: NodeParser, vector_store: Union[VectorStore, BasePydanticVectorStore]):
        """
        Initialize the pipeline with a file reader, node parser, and vector index manager.
        """
        self.file_parser = file_parser
        self.node_parser = node_parser
        self.vector_store = vector_store
        
    def execute(self, file_path: str, show_progress: bool = False):
        """
        Execute the digestion of the file.
        """
        # Load documents using the file reader
        documents = self.file_parser.load_data(file_path)

        # Parse nodes from the documents
        raw_nodes = self.node_parser.get_nodes_from_documents(documents=documents, show_progress=show_progress)

        # Get the nodes to index
        nodes_to_index = self._process_nodes(raw_nodes)

        # Add nodes to the vector index
        vector_index = self.vector_store.add(nodes=nodes_to_index)

        # TODO: Emit Message that the doc is ready to be chatted with.

    def _process_nodes(self, raw_nodes):
        """
        Process raw nodes based on the parser type.
        """
        if isinstance(self.node_parser, BaseElementNodeParser):
            # Get the text nodes and tables if the parser is capable of identifying both
            base_nodes, object_nodes = self.node_parser.get_nodes_and_objects(raw_nodes)
            return base_nodes + object_nodes
        else:
            return raw_nodes
