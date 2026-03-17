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