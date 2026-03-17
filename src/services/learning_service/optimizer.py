import sqlite3
from config.settings import BASE_DIR

class RankingOptimizer:
    def __init__(self):
        self.db_path = BASE_DIR / "data" / "databases" / "feedback.db"