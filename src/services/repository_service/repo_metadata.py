import json
from datetime import datetime
from pathlib import Path

class RepoMetadata:
    def __init__(self, repo_name, repo_url, path):
        self.metadata = {
            "repo_name": repo_name,
            "repo_url": repo_url,
            "indexed_at": datetime.now().isoformat(),
            "local_path": str(path),
            "stats": {
                "total_files": 0,
                "total_chunks": 0
            }
        }