import pytest
from unittest.mock import patch, MagicMock
from src.pipelines.query_pipeline import run_query

def test_full_query_pipeline_flow(mock_vector_store, mock_embedder):
    """
    Ensures the data flows from retrieval -> optimization -> prompt building
    without crashing, and correctly extracts Document objects.
    """
    
    with patch('src.pipelines.query_pipeline.AnswerGenerator') as MockGenerator:

        instance = MockGenerator.return_value
        instance.generate_answer.return_value = "This is a simulated AI response."
        
        query = "How does the virtual mouse handle clicks?"
        answer = run_query(query, mock_vector_store, mock_embedder)
        assert isinstance(answer, str)
        assert answer == "This is a simulated AI response."
        args, _ = instance.generate_answer.call_args
        actual_prompt = args[0]
        assert "def hello_world" in actual_prompt
        assert "How does the virtual mouse" in actual_prompt