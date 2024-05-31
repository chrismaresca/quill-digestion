from fastapi import FastAPI, File, UploadFile, HTTPException

# CORS Middleware
from fastapi.middleware.cors import CORSMiddleware

# Asyncronous context manager
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles resources before app startup (before requests come in) and after shutdown (once requests stop coming in)"""

    # Initialize the S3 Connection
    # S3ClientConnection.initialize()

    yield

# Main Application
app = FastAPI(lifespan=lifespan)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include Auth Router
app.include_router(auth_router)
