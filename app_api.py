from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from pathlib import Path
import threading

# Import your updated pipelines and services
from src.pipelines.ingest_pipeline import run_ingestion
from src.pipelines.query_pipeline import run_query
from src.services.embedding_service.embedder import Embedder
from src.services.vector_service.vector_store import VectorStore
from src.services.learning_service.feedback_collector import FeedbackCollector
from config.settings import VECTOR_DB_PATH

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_lock = threading.RLock()
_embedder: Embedder | None = None
_vector_stores: dict[str, VectorStore] = {}
_current_repo: str | None = None
_feedback_collector: FeedbackCollector | None = None