# Path
import asyncio
from pathlib import Path

# Import Llama Requirements
from llama_parse import LlamaParse
from llama_parse.utils import ResultType
from llama_index.core.llms.llm import LLM
from llama_index.core.node_parser import MarkdownElementNodeParser

# Import Pinecone client
from app.clients import PineconeClient, BaseVectorStoreClient, TextGenerationLLMClient


# Import Schemas
from app.schemas import DigestFilePayload, FileType

# Import the digestion pipeline
from app.pipelines import DigestionPipeline

# Import utilties
from app.utils import clean_filename

# Create a ORDER_COMPLETED_EVENT in redis streams


def digest_file(digest_file_payload: DigestFilePayload):
    """
    Function to digest a file.
    """

    # Get file type and path
    file_type = digest_file_payload.file_type
    file_path = digest_file_payload.file_path
    clean_file_name = clean_filename(filename=digest_file_payload.file_name)

    pc_client = PineconeClient()
    llm = TextGenerationLLMClient()

    if file_type == 'PDF':
        digest_pdf(pdf_file_path=file_path, vector_store_client=pc_client, llm=llm, file_name=clean_file_name)
    else:
        digest_excel(excel_file_path=file_path, vector_store_client=pc_client, file_name=clean_file_name)


def digest_pdf(pdf_file_path: Path,
               vector_store_client: BaseVectorStoreClient,
               llm: LLM,
               file_name: str,
               use_markdown: bool = True):
    """
    Wrapper for digesting the PDF files.
    """

    # Parser
    parser = LlamaParse(result_type="markdown" if use_markdown else ResultType.TXT)

    # Vector Store
    vector_store = vector_store_client.get_or_create_vector_store(namespace=file_name)

    # Node Parser
    node_parser = MarkdownElementNodeParser(llm=llm)

    # Create digestion pipeline and run.
    digestion_pipeline = DigestionPipeline(file_parser=parser, node_parser=node_parser, vector_index_manager=vector_store)



def digest_excel(excel_file_path: Path, vector_store_client: BaseVectorStoreClient, file_name: str, use_markdown: bool = True):
    """
    Wrapper for digesting the Exel files.
    """
    pass

# Define async functions
