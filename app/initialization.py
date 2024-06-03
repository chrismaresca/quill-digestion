# Typing
from typing import Literal, Tuple

# Config
from app.config import workmait_config

# Vector Store
from app.clients import PineconeClient, BaseVectorStoreClient

# LLM
from llama_index.core.llms import LLM
from llama_index.llms.huggingface import TextGenerationInference
from llama_index.llms.openai import OpenAI

# Embeddings
from llama_index.core.embeddings import BaseEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding


def initialize_clients(embedding_type: Literal["OpenAI", "HF"], llm_type: Literal["OpenAI", "HF"]) -> Tuple[BaseVectorStoreClient, LLM, BaseEmbedding]:
    pc_client = PineconeClient()

    if embedding_type == "OpenAI" and llm_type == "OpenAI":
        llm = OpenAI(api_key=workmait_config.OPENAI_API_KEY)
        embed_model = OpenAIEmbedding(api_key=workmait_config.OPENAI_API_KEY)
    elif embedding_type == "HF" and llm_type == "HF":
        llm = TextGenerationInference(model_url=workmait_config.HF_TEXT_GEN_INF_URL, token=workmait_config.HF_TOKEN)
        embed_model = HuggingFaceEmbedding(model_name=workmait_config.HF_EMBEDDING)
    else:
        raise ValueError("Invalid combination of embedding and LLM types")

    return pc_client, llm, embed_model
