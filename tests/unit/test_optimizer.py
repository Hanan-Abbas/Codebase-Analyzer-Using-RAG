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

    conn = sqlite3.connect(temp_db)
    conn.execute(
        "INSERT INTO feedback (chunk_id, rating) VALUES (?, ?)", 
        ("chunk_A", 1)
    )
    conn.commit()
    conn.close()
    
    # 3. Run the optimizer
    optimized = optimizer.boost_chunks(retrieved_chunks)
    
    # 4. Assertions
    # chunk_A should now be at the top (index 0) because of the boost
    assert optimized[0]["doc"].metadata["id"] == "chunk_A"
    assert optimized[0]["score"] > 0.5
    assert optimized[1]["score"] == 0.5