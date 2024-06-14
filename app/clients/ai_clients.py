from app.config import workmait_config

# LLM
from llama_index.llms.huggingface import TextGenerationInference
from llama_index.llms.openai import OpenAI

# Embeddings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

# Import Base LLM and Embedding
from llama_index.core.llms import LLM
from llama_index.core.embeddings import BaseEmbedding



class SingletonMeta(type):
    """
    A Singleton metaclass to ensure a class only has one instance per model name.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        key = (cls, kwargs.get('model_name'))
        if key not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[key] = instance
        return cls._instances[key]


class BaseAIClient(metaclass=SingletonMeta):
    def __init__(self, model_name=None, **kwargs):
        self.model_name = model_name
        self.llm: LLM = None
        self.embedding: BaseEmbedding = None
        self.llm_kwargs = kwargs.get('llm_kwargs', {})
        self.embedding_kwargs = kwargs.get('embedding_kwargs', {})

    def initialize_llm(self):
        raise NotImplementedError("Subclasses should implement this method to initialize LLM.")

    def initialize_embedding(self):
        raise NotImplementedError("Subclasses should implement this method to initialize embedding.")


class OpenAIClient(BaseAIClient):
    def __init__(self, model_name=None, **kwargs):
        super().__init__(model_name, **kwargs)
        if self.model_name is None:
            self.model_name = workmait_config.OPENAI_DEFAULT_MODEL
        self.initialize_llm()
        self.initialize_embedding()

    def initialize_llm(self):
        self.llm = OpenAI(model=self.model_name, api_key=workmait_config.OPENAI_API_KEY, **self.llm_kwargs)

    def initialize_embedding(self):
        self.embedding = OpenAIEmbedding(api_key=workmait_config.OPENAI_API_KEY, **self.embedding_kwargs)


class HFClient(BaseAIClient):
    def __init__(self, model_name=None, **kwargs):
        super().__init__(model_name, **kwargs)
        if self.model_name is None:
            self.model_name = workmait_config.HF_EMBEDDING
        self.initialize_llm()
        self.initialize_embedding()

    def initialize_llm(self):
        self.llm = TextGenerationInference(model_url=workmait_config.HF_TEXT_GEN_INF_URL, token=workmait_config.HF_TOKEN, **self.llm_kwargs)

    def initialize_embedding(self):
        self.embedding = HuggingFaceEmbedding(model_name=self.model_name, **self.embedding_kwargs)
