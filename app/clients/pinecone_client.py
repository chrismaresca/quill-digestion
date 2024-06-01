# ABC
from abc import ABC, abstractmethod

# Pinecone 
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore

# Import Config
from app.config import workmait_config


class BaseVectorStoreClient(ABC):
    """Abstract base class for vector store clients."""

    @abstractmethod
    def initialize(cls):
        """Initialize the vector store client connection."""
        pass

    @abstractmethod
    def get_index(cls):
        """Return the vector store index instance, initializing if not already done."""
        pass

    @abstractmethod
    def get_or_create_vector_store(cls, namespace):
        """Return the existing vector store for the namespace or create a new one."""
        pass


class PineconeClient(BaseVectorStoreClient):
    """Manages Pinecone connections, providing the Pinecone index and vector store."""
    _index_instance = None
    _vector_stores = {}

    @classmethod
    def initialize(cls):
        """Initialize the Pinecone client connection."""
        if cls._index_instance is None:
            # Get the API Key
            api_key = workmait_config.PC_API_KEY
            # Get the host
            host = workmait_config.PC_HOST
            # Initialize Pinecone
            pc = Pinecone(api_key=api_key)
            cls._index_instance = pc.Index(name='workmait-aws', host=host)

    @classmethod
    def get_index(cls):
        """Return the Pinecone index instance, initializing if not already done."""
        if cls._index_instance is None:
            cls.initialize()  # Ensure it is initialized
        return cls._index_instance

    @classmethod
    def get_or_create_vector_store(cls, namespace) -> PineconeVectorStore:
        """Return the existing vector store for the namespace or create a new one."""
        if namespace not in cls._vector_stores:
            index = cls.get_index()
            cls._vector_stores[namespace] = PineconeVectorStore(
                pinecone_index=index, namespace=namespace)
        return cls._vector_stores[namespace]


