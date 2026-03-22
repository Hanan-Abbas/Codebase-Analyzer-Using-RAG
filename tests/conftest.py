import pytest
from unittest.mock import MagicMock
import numpy as np

@pytest.fixture
def mock_embedder():
    """Returns a fake embedder so tests don't download models."""
    embedder = MagicMock()
    embedder.generate_embeddings.return_value = np.random.rand(1, 384).tolist()
    return embedder

@pytest.fixture
def mock_vector_store():
    """Returns a fake vector store with mock metadata."""
    v_store = MagicMock()
    mock_doc = MagicMock()
    mock_doc.page_content = "def hello_world(): print('hi')"
    mock_doc.metadata = {"id": "test_chunk_001", "source": "main.py"}
    
    v_store.metadata = {0: mock_doc}
    v_store.index.search.return_value = (np.array([[0.1]]), np.array([[0]]))
    return v_store

@pytest.fixture
def temp_db(tmp_path):
    """Creates a temporary feedback database for testing."""
    db_path = tmp_path / "test_feedback.db"
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE feedback (
            id INTEGER PRIMARY KEY,
            question TEXT,
            answer TEXT,
            chunk_id TEXT,
            rating INTEGER,
            timestamp TEXT
        )
    """)
    conn.close()
    return db_path