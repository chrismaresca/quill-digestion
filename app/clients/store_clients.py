from abc import ABC, abstractmethod
from typing import Any, Dict

# Clients
import neo4j
from pinecone import Pinecone

# Llama
from app.common.llama import PineconeVectorStore, Neo4jPropertyGraphStore


from app.config import workmait_config


# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# ABC


class BaseStoreClient(ABC):
    """Abstract base class for store clients."""

    @abstractmethod
    def initialize(self):
        """Initialize the store client connection."""
        pass

    @abstractmethod
    def get_or_create_store(self, namespace: str):
        """Return the existing store for the namespace or create a new one."""
        pass

    @abstractmethod
    def close(self):
        """Close the store client connection."""
        pass

# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# Neo4j


class Neo4jClient(BaseStoreClient):
    _driver = None
    _stores: Dict[str, Neo4jPropertyGraphStore] = {}

    @classmethod
    def initialize(cls, **neo4j_kwargs: Any):
        """Initialize the Neo4j driver."""
        if not cls._driver:
            username = workmait_config.NEO4J_USERNAME
            password = workmait_config.NEO4J_PASSWORD
            url = workmait_config.NEO4J_URL
            cls._driver = neo4j.GraphDatabase.driver(url, auth=(username, password), **neo4j_kwargs)

    @classmethod
    def get_or_create_store(cls, namespace: str):
        """Return the existing graph store for the namespace or create a new one."""
        if namespace not in cls._stores:
            username = workmait_config.NEO4J_USERNAME
            password = workmait_config.NEO4J_PASSWORD
            url = workmait_config.NEO4J_URL
            cls._stores[namespace] = Neo4jPropertyGraphStore(
                username=username,
                password=password,
                url=url,
                database=namespace
            )
        return cls._stores[namespace]

    @classmethod
    def get_driver(cls):
        """Return the Neo4j driver instance, initializing if not already done."""
        if cls._driver is None:
            cls.initialize()
        return cls._driver

    @classmethod
    def close(cls):
        """Close the Neo4j driver."""
        if cls._driver is not None:
            cls._driver.close()
        for store in cls._stores.values():
            store.client.close()

# ------------------------------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------------------------------- #
# Pinecone


class PineconeClient(BaseStoreClient):
    _index_instance: Pinecone.Index = None
    _vector_stores: Dict[str, PineconeVectorStore] = {}

    @classmethod
    def initialize(cls) -> None:
        """Initialize the Pinecone client connection."""
        if cls._index_instance is None:
            api_key = workmait_config.PC_API_KEY
            host = workmait_config.PC_HOST
            pc = Pinecone(api_key=api_key)
            cls._index_instance = pc.Index(name='workmait-aws', host=host)

    @classmethod
    def get_or_create_store(cls, namespace: str) -> PineconeVectorStore:
        """Return the existing vector store for the namespace or create a new one."""
        if namespace not in cls._vector_stores:
            index = cls.get_index()
            cls._vector_stores[namespace] = PineconeVectorStore(pinecone_index=index, namespace=namespace)
        return cls._vector_stores[namespace]

    @classmethod
    def get_index(cls) -> Pinecone.Index:
        """Return the Pinecone index instance, initializing if not already done."""
        if cls._index_instance is None:
            cls.initialize()
        return cls._index_instance

    @classmethod
    def close(cls):
        """Close the Pinecone client connection."""
        pass
