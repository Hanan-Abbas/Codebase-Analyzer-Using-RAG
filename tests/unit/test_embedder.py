import pytest
import numpy as np
from src.services.embedding_service.embedder import Embedder

def test_embedder_output_dimensions():
    """
    Ensures the embedder produces a list of vectors with 
    the correct dimensionality (384 for MiniLM).
    """
    embedder = Embedder()
    test_text = ["This is a test sentence."]
    
    embeddings = embedder.generate_embeddings(test_text)
    
    # Check if output is a list/array
    assert isinstance(embeddings, (list, np.ndarray))
    # Check dimensions (MiniLM-L6-v2 always outputs 384)
    assert len(embeddings[0]) == 384

def test_embedder_multiple_inputs():
    """
    Ensures the embedder can handle multiple sentences at once.
    """
    embedder = Embedder()
    test_texts = ["Sentence one", "Sentence two", "Sentence three"]
    
    embeddings = embedder.generate_embeddings(test_texts)
    
    assert len(embeddings) == 3
    assert len(embeddings[0]) == 384