import pytest
from src.services.vector_service.retriever import Retriever

def test_retriever_returns_correct_structure(mock_vector_store, mock_embedder):
    """
    Test if the retriever returns a list of dictionaries 
    containing 'doc' and 'score' keys.
    """
    retriever = Retriever(mock_vector_store, mock_embedder)
    query = "How do I control the mouse?"
    
    results = retriever.get_relevant_chunks(query, top_k=1)
    
    # Check that we got a list
    assert isinstance(results, list)
    assert len(results) == 1
    
    # Check the dictionary structure we fixed earlier
    assert "doc" in results[0]
    assert "score" in results[0]
    
    # Verify the document metadata is accessible
    assert results[0]["doc"].metadata["id"] == "test_chunk_001"