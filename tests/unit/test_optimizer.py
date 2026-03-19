import pytest
from unittest.mock import MagicMock
from src.services.learning_service.optimizer import RankingOptimizer
import sqlite3

def test_optimizer_boosts_helpful_chunks(temp_db):
    """
    Test that a chunk with positive feedback gets a higher score.
    """
    optimizer = RankingOptimizer()
    optimizer.db_path = temp_db
s
    doc_a = MagicMock()
    doc_a.metadata = {"id": "chunk_A"}
    
    doc_b = MagicMock()
    doc_b.metadata = {"id": "chunk_B"}
    
    retrieved_chunks = [
        {"doc": doc_a, "score": 0.5},
        {"doc": doc_b, "score": 0.5}
    ]