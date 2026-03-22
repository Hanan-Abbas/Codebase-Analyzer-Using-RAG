import os
from pathlib import Path
from tqdm import tqdm

from src.services.repository_service.clone_repo import RepoCloner
from src.services.repository_service.repo_metadata import RepoMetadata
from src.services.processing_service.code_cleaner import CodeCleaner
from src.services.processing_service.code_chunker import CodeChunker
from src.services.embedding_service.embedder import Embedder
from src.services.vector_service.vector_store import VectorStore
from config.settings import SUPPORTED_EXTENSIONS, IGNORE_DIRS, VECTOR_DB_PATH

def run_ingestion(repo_url, embedder: Embedder | None = None, force_reindex: bool = False):
    cloner = RepoCloner(repo_url)
    repo_name = cloner.repo_name
    index_dir = Path(VECTOR_DB_PATH) / repo_name
    index_file = index_dir / "index.faiss"
    metadata_file = index_dir / "metadata.pkl"

    # Fast path: if we already have an on-disk index, reuse it.
    # (This avoids re-cloning, re-chunking, and re-embedding.)
    if not force_reindex and index_file.exists() and metadata_file.exists():
        return VectorStore.load(repo_name)

    repo_path = cloner.clone()
    if not repo_path:
        return None

    all_chunks = []
    physical_map = [] 

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), repo_path)
            physical_map.append(rel_path) # LOG EVERYTHING FOR VERIFICATION
            
            if os.path.splitext(file)[1] in SUPPORTED_EXTENSIONS:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    chunker = CodeChunker(os.path.splitext(file)[1])
                    # Pass the relative path for breadcrumbs
                    chunks = chunker.chunk_text(content, {"file_path": rel_path})
                    all_chunks.extend(chunks)
                except Exception: continue

    embedder = embedder or Embedder()
    embeddings = embedder.generate_embeddings([doc.page_content for doc in all_chunks])
    
    store = VectorStore(dimension=embedder.get_dimension())
    store.add_to_index(embeddings, all_chunks)
    store.set_file_structure(physical_map)
    store.save(repo_name)
    return store