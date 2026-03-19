import pytest
from unittest.mock import MagicMock
import numpy as np

@pytest.fixture
def mock_embedder():
    """Returns a fake embedder so tests don't download models."""
    embedder = MagicMock()
    # Simulate a 384-dimension vector (standard for MiniLM)
    embedder.generate_embeddings.return_value = np.random.rand(1, 384).tolist()
    return embedder

@pytest.fixture
def mock_vector_store():
    """Returns a fake vector store with mock metadata."""
    v_store = MagicMock()
    # Create a mock document object
    mock_doc = MagicMock()
    mock_doc.page_content = "def hello_world(): print('hi')"
    mock_doc.metadata = {"id": "test_chunk_001", "source": "main.py"}
    
    v_store.metadata = {0: mock_doc}
    # Mock FAISS search: returns distance 0.1 and index 0
    v_store.index.search.return_value = (np.array([[0.1]]), np.array([[0]]))
    return v_store