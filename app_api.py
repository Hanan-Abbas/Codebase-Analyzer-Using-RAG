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

@app.post("/ingest")
async def ingest(request: IngestRequest):
    try:
        repo_name = _get_repo_name(request.url)

        with _lock:
            global _current_repo

            # If it's already active and cached, do nothing.
            if _current_repo == repo_name and repo_name in _vector_stores:
                return {"status": "success", "message": f"✅ {repo_name} already loaded (cached)."}

            # If cached from a previous request, reuse instantly.
            if repo_name in _vector_stores:
                _current_repo = repo_name
                return {"status": "success", "message": f"✅ {repo_name} loaded from memory cache."}

        # If an on-disk index exists, load it (fast) and cache it.
        if _index_exists(repo_name):
            store = VectorStore.load(repo_name)
            with _lock:
                _vector_stores[repo_name] = store
                _current_repo = repo_name
            return {"status": "success", "message": f"✅ {repo_name} loaded from disk index (cached in memory)."}

        # Otherwise, ingest (slow path), then cache.
        store = run_ingestion(request.url, embedder=_get_embedder(), force_reindex=False)
        if not store:
            raise HTTPException(status_code=500, detail="Ingestion failed to return a valid store.")

        with _lock:
            _vector_stores[repo_name] = store
            _current_repo = repo_name
        return {"status": "success", "message": f"✅ {repo_name} indexed and cached."}
    except Exception as e:
        print(f"INGEST ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):

    with _lock:
        store = _vector_stores.get(_current_repo) if _current_repo else None
    if not store:
        return {"answer": "⚠️ No repository indexed yet. Please paste a GitHub URL in the top bar first."}
    
    try:

        answer = run_query(
            query=request.prompt, 
            vector_store=store, 
            embedder=_get_embedder()
        )
        return {"answer": answer}
    except Exception as e:
        print(f"CHAT ERROR: {e}")
        return {"answer": f"❌ Backend Error: {str(e)}"}


@app.get("/health")
async def health():
    with _lock:
        loaded_repos = list(_vector_stores.keys())
        current_repo = _current_repo
        embedder_loaded = _embedder is not None
    return {
        "status": "ok",
        "embedder_loaded": embedder_loaded,
        "current_repo": current_repo,
        "cached_repos": loaded_repos,
    }



@app.post("/feedback")
async def feedback(request: FeedbackRequest):
    """Store explicit user feedback so RankingOptimizer can learn over time."""
    if request.rating not in (0, 1):
        raise HTTPException(status_code=400, detail="rating must be 0 or 1")

    global _feedback_collector
    with _lock:
        if _feedback_collector is None:
            _feedback_collector = FeedbackCollector()
        collector = _feedback_collector

    try:
        collector.save_feedback(request.question, request.answer, request.rating)
        return {"status": "ok"}
    except Exception as e:
        print(f"FEEDBACK ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)