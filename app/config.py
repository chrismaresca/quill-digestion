# Load Environment variables
import os
from dotenv import load_dotenv

# Pydantic
from pydantic import BaseModel

# Load the environment variables
load_dotenv()


class WorkmaitConfig(BaseModel):

    # MongoDB
    MONGO_CONNECTION_STR: str = os.getenv('MONGO_CONNECTION_STR')
    
    LLAMA_PARSE_API: str = os.getenv('LLAMA_PARSE_API')
    LLAMA_PARSE_API_KEY: str = os.getenv('LLAMA_PARSE_API_KEY')


    # Google
    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET')

    # Pinecone
    PC_API_KEY: str = os.getenv('PC_API_KEY')
    PC_HOST: str = os.getenv('PC_HOST')

    # HF
    HF_TEXT_GEN_INF_URL: str = os.getenv('HF_TEXT_GEN_INF_URL')
    HF_TOKEN: str = os.getenv('HF_TOKEN')

    # OpenAI API KEY
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')

    # Boto3
    AWS_ACCESS_KEY_ID: str = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY')


# Instance of config
workmait_config = WorkmaitConfig()
