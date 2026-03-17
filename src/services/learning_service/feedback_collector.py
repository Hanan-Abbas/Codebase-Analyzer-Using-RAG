import sqlite3
from datetime import datetime
from config.settings import BASE_DIR

class FeedbackCollector:
    def __init__(self):
        self.db_path = BASE_DIR / "data" / "databases" / "feedback.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            # We add chunk_id to track which specific code piece was used
            conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    answer TEXT,
                    chunk_id TEXT,  
                    rating INTEGER,
                    timestamp TEXT
                )
            """)

    def save_feedback(self, question, answer, rating):
        """Rating: 1 for Good, 0 for Bad"""
        # Indented 4 spaces
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO feedback (question, answer, rating, timestamp) VALUES (?, ?, ?, ?)",
                (question, answer, rating, datetime.now().isoformat())
            )
        print(f"\n[Learning Service] Feedback saved to local database.")