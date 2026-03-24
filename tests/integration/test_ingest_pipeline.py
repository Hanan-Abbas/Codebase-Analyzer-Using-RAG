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
        
        mock_walk.return_value = [
            ('/tmp/repo', [], ['main.py'])
        ]

        with patch('src.pipelines.ingest_pipeline.Embedder') as MockEmbedder:
            MockEmbedder.return_value.generate_embeddings.return_value = [[0.1] * 384]
            
            repo_url = "https://github.com/user/fake"

            vector_store = run_ingestion(repo_url)
            
            # 4. Assertions
            assert mock_clone.called
            assert vector_store is not None
            MockVectorStore.return_value.save.assert_called_with("fake")