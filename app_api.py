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

def _get_repo_name(url: str) -> str:
    return url.rstrip("/").split("/")[-1].replace(".git", "")

def _get_embedder() -> Embedder:
    global _embedder
    with _lock:
        if _embedder is None:
            _embedder = Embedder()
        return _embedder

def _index_exists(repo_name: str) -> bool:
    p = Path(VECTOR_DB_PATH) / repo_name
    return (p / "index.faiss").exists() and (p / "metadata.pkl").exists()

class IngestRequest(BaseModel):
    url: str

class ChatRequest(BaseModel):
    prompt: str


class FeedbackRequest(BaseModel):
    question: str
    answer: str
    rating: int  # 1 = good, 0 = bad