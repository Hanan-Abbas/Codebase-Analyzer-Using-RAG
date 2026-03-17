import sqlite3
from config.settings import BASE_DIR

class RankingOptimizer:
    def __init__(self):
        self.db_path = BASE_DIR / "data" / "databases" / "feedback.db"

    def boost_chunks(self, retrieved_chunks):
        """
        Expects: [{"doc": Document, "score": float}, ...]
        Returns: Re-sorted list of the same dictionaries.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            optimized_chunks = []