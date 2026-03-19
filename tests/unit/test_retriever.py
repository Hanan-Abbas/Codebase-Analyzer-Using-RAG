import pytest
from src.services.vector_service.retriever import Retriever

def test_retriever_returns_correct_structure(mock_vector_store, mock_embedder):
    """
    Test if the retriever returns a list of dictionaries 
    containing 'doc' and 'score' keys.