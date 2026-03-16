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
    
    def generate_embeddings(self, texts):
        # Ensure no gradients are calculated (saves memory/CPU cycles)
        with torch.no_grad():
            embeddings = self.model.encode(
                texts, 
                normalize_embeddings=True, 
                show_progress_bar=False
            )
        return embeddings

    def get_dimension(self):
        return self.model.get_sentence_embedding_dimension()