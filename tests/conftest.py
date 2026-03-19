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