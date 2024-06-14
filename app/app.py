# # FastAPI
# from fastapi import FastAPI

# # CORS Middleware
# from fastapi.middleware.cors import CORSMiddleware

# # Asyncronous context manager
# from contextlib import asynccontextmanager

# # Import routers
# from app.routers.digest import digest_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     """Handles resources before app startup (before requests come in) and after shutdown (once requests stop coming in)"""

#     # Initialize the S3 Connection
#     # S3ClientConnection.initialize()

#     yield

# # Main Application
# app = FastAPI(lifespan=lifespan)


# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods
#     allow_headers=["*"],  # Allows all headers
# )

# # Include Digest Router
# app.include_router(digest_router)


# app/main.py

from fastapi import FastAPI

# CORS Middleware
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
import asyncio

from app.clients import RedisClient, PineconeClient, Neo4jClient
from app.common.initialization import initialize_strategies
from app.strategies import vector_strategies, graph_strategies
from app.consumers import consume_add_nodes, consume_delete_nodes, consume_move_nodes, consume_delete_store


@asynccontextmanager
async def lifespan(app: FastAPI):

    redis_client = RedisClient()

    # Initialize store clients and pipelines
    initialize_strategies(vector_strategies=vector_strategies, graph_strategies=graph_strategies)

    # Start consumers for each event
    add_nodes_task = asyncio.create_task(consume_add_nodes(redis_client))
    delete_nodes_task = asyncio.create_task(consume_delete_nodes(redis_client))
    delete_store_task = asyncio.create_task(consume_delete_store(redis_client))
    move_nodes_task = asyncio.create_task(consume_move_nodes(redis_client))

    yield

    # Cancel the background tasks during shutdown
    tasks = [add_nodes_task, delete_nodes_task, delete_store_task, move_nodes_task]
    for task in tasks:
        task.cancel()

    # Await the tasks to ensure proper shutdown
    await asyncio.gather(*tasks, return_exceptions=True)    # Close store clients

    PineconeClient.close()
    Neo4jClient.close()
    
    redis_client.close()



app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Define your routes here
@app.get("/")
async def read_root():
    return {"message": "Hello World"}
