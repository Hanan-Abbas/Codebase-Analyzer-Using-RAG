import torch
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

class Embedder:
    def __init__(self):
        # Force torch to only see CPU before loading model
        device = "cpu"
        print(f"Loading embedding model: {EMBEDDING_MODEL} on {device.upper()}...")
        
        # Load model explicitly on CPU
        self.model = SentenceTransformer(EMBEDDING_MODEL, device=device)