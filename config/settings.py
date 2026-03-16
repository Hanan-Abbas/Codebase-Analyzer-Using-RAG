import os


# Model Config
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Fast for local dev
LLM_MODEL = "llama3" # Ensure you have this pulled in Ollama

# Extraction Config
SUPPORTED_EXTENSIONS = {'.py', '.js', '.ts', '.java', '.cpp', '.md', '.json', '.yml', '.yaml', '.dockerfile'}
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', 'dist', 'build', 'env'}

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")