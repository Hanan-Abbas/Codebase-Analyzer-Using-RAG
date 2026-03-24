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