# ABC
from abc import ABC, abstractmethod
from typing import Dict, Any, List


from app.payloads import AddNodesPayload, FilePayload


class SingletonMeta(type):
    """
    A metaclass for creating Singleton classes.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        When called, creates instance if does not exist. Else, it returns instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class BasePipeline(ABC, metaclass=SingletonMeta):
    """
    Abstract base class for pipelines.
    """
    _pipeline_instances: Dict[str, 'BasePipeline'] = {}

    def __init__(self, strategy_name: str, pipeline_type: str):
        self._strategy_name = strategy_name
        self._pipeline_type = pipeline_type

    @property
    def strategy_name(self) -> str:
        return self._strategy_name

    @property
    def pipeline_type(self) -> str:
        return self._pipeline_type

    @abstractmethod
    def execute(self,
                store_namespace: str,
                file_payloads: List[FilePayload],
                payload_metadata: Dict[str, Any] = None,
                **kwargs):
        """Execute the pipeline."""
        pass

    @classmethod
    @abstractmethod
    def create_pipeline(cls, strategy_name: str, **kwargs):
        """Factory method to create pipeline components."""
        pass

    @classmethod
    def register_pipeline(cls, strategy_name: str, pipeline_instance: 'BasePipeline'):
        """Register a pipeline instance."""
        cls._pipeline_instances[strategy_name] = pipeline_instance

    @classmethod
    def get_pipeline(cls, strategy_name: str) -> 'BasePipeline':
        """Retrieve a pipeline instance by strategy name."""
        pipeline_instance = cls._pipeline_instances.get(strategy_name)
        if not pipeline_instance:
            raise ValueError(f"No pipeline registered under strategy: {strategy_name}")
        return pipeline_instance


# --------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------- #
# --------------------------------------------------------------------------------------------------------------- #
