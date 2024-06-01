
# Import Config
from app.config import workmait_config

from llama_index.llms.huggingface import TextGenerationInference

from llama_index.core.base.llms.types import (
    ChatMessage,
    MessageRole,
)


class TextGenerationLLMClient:
    """Singleton class for accessing the text generation LLM."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure only one instance of the LLM client is created."""
        if cls._instance is None:
            cls._instance = super(TextGenerationLLMClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the LLM client with the model URL and token."""
        # Get the configuration
        hf_token = workmait_config.HF_TOKEN
        hf_text_gen_inf_url = workmait_config.HF_TEXT_GEN_INF_URL
        self.model = TextGenerationInference(model_url=hf_text_gen_inf_url, token=hf_token)

    def __getattr__(self, name):
        """Delegate attribute access to the model instance."""
        return getattr(self.model, name)
