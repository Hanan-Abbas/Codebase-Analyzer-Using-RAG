import pytest
import sqlite3
import os
from unittest.mock import MagicMock
from src.services.learning_service.feedback_collector import FeedbackCollector
from src.services.learning_service.optimizer import RankingOptimizer@pytest.fixture


def temp_db(tmp_path):
    """Creates a temporary SQLite database for testing."""
    db_file = tmp_path / "test_feedback.db"
    # Initialize the table structure
    conn = sqlite3.connect(db_file)
    conn.execute("""
        CREATE TABLE feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            chunk_id TEXT,
            rating INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    return str(db_file)

def test_feedback_collection(temp_db):
    """Test that feedback is correctly saved to the database."""
    collector = FeedbackCollector(db_path=temp_db)

    # Simulate a user giving a thumbs up (rating=1)
    collector.save_feedback(
        query="How does auth work?",
        chunk_id="auth_service.py_chunk_1",
        rating=1
    )

    # Verify it exists in the DB
    conn = sqlite3.connect(temp_db)
    cursor = conn.execute("SELECT chunk_id, rating FROM feedback")
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == "auth_service.py_chunk_1"
    assert row[1] == 1

def test_optimizer_ranking_with_feedback(temp_db):
    """Test that the optimizer correctly identifies and boosts high-rated chunks."""
    # 1. Setup feedback in DB
    conn = sqlite3.connect(temp_db)
    conn.execute("INSERT INTO feedback (chunk_id, rating) VALUES (?, ?)", ("target_chunk", 1))
    conn.commit()
    conn.close()
    
    optimizer = RankingOptimizer(db_path=temp_db)
    
    # 2. Mock some retrieved chunks
    doc_hit = MagicMock()
    doc_hit.metadata = {"id": "target_chunk"}
    
    doc_miss = MagicMock()
    doc_miss.metadata = {"id": "other_chunk"}
    
    results = [
        {"doc": doc_hit, "score": 0.4},
        {"doc": doc_miss, "score": 0.4}
    ]