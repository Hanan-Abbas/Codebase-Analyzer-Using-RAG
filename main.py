import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align

# Internal Pipeline & Service Imports
from src.pipelines.ingest_pipeline import run_ingestion
from src.pipelines.query_pipeline import run_query
from src.services.embedding_service.embedder import Embedder
from src.services.vector_service.vector_store import VectorStore
from src.services.learning_service.feedback_collector import FeedbackCollector
from src.services.repository_service.repo_metadata import RepoMetadata
from src.ui import CLIChat  # Ensure src/ui/__init__.py has: from .cli_chat import CLIChat

console = Console()

def display_welcome():
    """Renders the RepoMind branding."""
    console.print("\n")
    panel = Panel(
        "[bold cyan]RepoMind v1.0[/bold cyan]\n[white]Your AI-Powered Codebase Navigator[/white]",
        border_style="bold blue",
        padding=(1, 2),
        expand=False
    )
    console.print(Align.center(panel))
    console.print("\n")

def main():
    display_welcome()