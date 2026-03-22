import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Best-effort .env loading:
# 1) Try python-dotenv if available
# 2) Fallback to a simple manual parser
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv(BASE_DIR / ".env")
except Exception:
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        try:
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())
        except Exception:
            # If even this fails, we silently fall back to system env vars only.
            pass
REPO_STORAGE = BASE_DIR / "data" / "repos"
VECTOR_DB_PATH = BASE_DIR / "data" / "vectors"

# Chunking Config
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Model Config
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")  # Fast for local dev

# Extraction Config
SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.cpp', '.md', '.json', '.yml', '.yaml', '.dockerfile'}
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', 'dist', 'build', 'env'}

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")