# app/dependencies.py
from fastapi import Depends
from app.initialization import initialize_clients


def get_digestion_clients():
    return initialize_clients(embedding_type="OpenAI", llm_type="OpenAI")

