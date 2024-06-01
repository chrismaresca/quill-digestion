# Path
import asyncio
from pathlib import Path

# Import Llama Requirements
from llama_parse import LlamaParse
from llama_parse.utils import ResultType
from llama_index.core.llms.llm import LLM
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.llms.huggingface import TextGenerationInference
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.huggingface import HuggingFaceInferenceAPIEmbedding

# Import Pinecone client
from app.clients import PineconeClient, BaseVectorStoreClient, TextGenerationLLMClient

# Import Events
from app.events import EVENT_TYPE_DIGEST_COMPLETE, pubsub_manager

# Import Schemas
from app.schemas import DigestFilePayload, FileType, DigestFileCompletePayload

# Import the digestion pipeline
from app.pipelines import DigestionPipeline

# Import utilties
from app.utils import clean_filename

# Import config
from app.config import workmait_config


hf_token = workmait_config.HF_TOKEN
hf_text_gen_inf_url = workmait_config.HF_TEXT_GEN_INF_URL

# TODO: Handle this better
pc_client = PineconeClient()
llm = TextGenerationInference(model_url=hf_text_gen_inf_url, token=hf_token)
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


def digest_file(digest_file_payload: DigestFilePayload, vector_store_client: BaseVectorStoreClient = pc_client, llm: LLM = llm, embed_model: BaseEmbedding = embed_model):
    """
    Function to digest a file.
    """

    # Get file type and path
    file_type = digest_file_payload.file_type
    file_path = digest_file_payload.file_path
    clean_file_name = clean_filename(filename=digest_file_payload.file_name)

    if file_type == 'PDF':
        result = digest_pdf(pdf_file_path=file_path, vector_store_client=vector_store_client, llm=llm, file_name=clean_file_name, embed_model=embed_model)
    else:
        result = digest_excel(excel_file_path=file_path, vector_store_client=vector_store_client, file_name=clean_file_name, embed_model=embed_model)

    # Create a payload for the event
    event_payload = DigestFileCompletePayload(file_name=clean_file_name, status="completed")

    # publish the payload for the event
    pubsub_manager.publish(EVENT_TYPE_DIGEST_COMPLETE, event_payload.model_dump())

    return result


def digest_pdf(pdf_file_path: Path,
               vector_store_client: BaseVectorStoreClient,
               llm: LLM,
               embed_model: BaseEmbedding,
               file_name: str,
               use_markdown: bool = True):
    """
    Wrapper for digesting the PDF files.
    """

    # Parser
    parser = LlamaParse(result_type="markdown" if use_markdown else ResultType.TXT, api_key=workmait_config.LLAMA_PARSE_API_KEY)

    # Vector Store
    vector_store = vector_store_client.get_or_create_vector_store(namespace=file_name)

    # Node Parser
    node_parser = MarkdownElementNodeParser(llm=llm)

    # Create digestion pipeline and run.
    digestion_pipeline = DigestionPipeline(file_parser=parser, node_parser=node_parser, vector_store=vector_store, embed_model=embed_model)

    # Execute
    digestion_pipeline.execute(file_path=pdf_file_path, show_progress=False)

    return {"status": "completed", "file_name": file_name}


def digest_excel(excel_file_path: Path,
                 vector_store_client: BaseVectorStoreClient,
                 llm: LLM,
                 embed_model: BaseEmbedding,
                 file_name: str,
                 use_markdown: bool = True):
    """
    Wrapper for digesting the Exel files.
    """
    # TODO: Logic for excel here
    return {"status": "completed", "file_name": file_name}
