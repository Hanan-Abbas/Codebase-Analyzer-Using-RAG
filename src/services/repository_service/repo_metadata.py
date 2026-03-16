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

    def save(self, output_dir):
        meta_path = Path(output_dir) / "metadata.json"
        with open(meta_path, "w") as f:
            json.dump(self.metadata, f, indent=4)

    @staticmethod
    def load(output_dir):
        meta_path = Path(output_dir) / "metadata.json"
        if meta_path.exists():
            with open(meta_path, "r") as f:
                return json.load(f)
        return Non