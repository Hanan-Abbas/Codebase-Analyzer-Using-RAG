import pytest
from unittest.mock import patch, MagicMock
from src.pipelines.ingest_pipeline import run_ingestion


def test_ingest_pipeline_logic():
    # 1. Patch all the "Side Effects" (Git, File System, Metadata Saving)
    with patch('git.Repo.clone_from') as mock_clone, \
         patch('os.walk') as mock_walk, \
         patch('pathlib.Path.read_text', return_value="print('hi')"), \
         patch('src.pipelines.ingest_pipeline.VectorStore') as MockVectorStore, \
         patch('src.pipelines.ingest_pipeline.RepoMetadata') as MockMetadata: