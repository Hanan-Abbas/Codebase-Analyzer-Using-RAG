import pytest
import sqlite3
from unittest.mock import MagicMock
from src.services.learning_service.optimizer import RankingOptimizer

def test_optimizer_boosts_helpful_chunks(temp_db):
    """
    Test that a chunk with positive feedback gets a higher score.
    """
    optimizer = RankingOptimizer()
    optimizer.db_path = temp_db 
    
    doc_a = MagicMock()
    doc_a.metadata = {"id": "chunk_A"}
    
    doc_b = MagicMock()
    doc_b.metadata = {"id": "chunk_B"}
    retrieved_chunks = [
        {"doc": doc_a, "score": 0.5},
        {"doc": doc_b, "score": 0.5}
    ]

    conn = sqlite3.connect(temp_db)
    conn.execute("CREATE TABLE IF NOT EXISTS feedback (chunk_id TEXT, rating INTEGER)")
    conn.execute(
        "INSERT INTO feedback (chunk_id, rating) VALUES (?, ?)", 
        ("chunk_A", 1)
    )
    conn.commit()
    conn.close()

    optimized = optimizer.boost_chunks(retrieved_chunks)

    assert optimized[0]["doc"].metadata["id"] == "chunk_A", "Chunk A should be boosted to the top"
    assert optimized[0]["score"] > 0.5, "Chunk A score should increase"
    assert optimized[1]["score"] == 0.5, "Chunk B score should remain unchanged"