# Import Schemas
from app.schemas import DigestDocsPayload

# Create a ORDER_COMPLETED_EVENT in redis streams
def digest_docs(digest_docs_payload: DigestDocsPayload):
    """
    Function to digest the docs and then prepare it for querying.
    """

    # 
    pass