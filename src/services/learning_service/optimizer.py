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

            for item in retrieved_chunks:
                # FIX: Access the Document object from the dict first
                doc_obj = item['doc'] 
                
                # Get the chunk_id from the Document's metadata
                chunk_id = doc_obj.metadata.get("id", "unknown")
                
                # Check for positive feedback
                cursor.execute(
                    "SELECT COUNT(*) FROM feedback WHERE chunk_id = ? AND rating = 1",
                    (chunk_id,)
                )
                boost_count = cursor.fetchone()[0] 
                item['score'] += (boost_count * 0.05) 
                optimized_chunks.append(item)

        # Sort by the new boosted score (descending)
        return sorted(optimized_chunks, key=lambda x: x['score'], reverse=True)