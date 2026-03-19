import pytest
from unittest.mock import patch, MagicMock
from src.pipelines.query_pipeline import run_query

def test_full_query_pipeline_flow(mock_vector_store, mock_embedder):
    """
    Ensures the data flows from retrieval -> optimization -> prompt building
    without crashing, and correctly extracts Document objects.
    """