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

    # --- 1. INITIALIZATION ---
    repo_url = Prompt.ask("[bold yellow]Enter the GitHub Repository URL[/bold yellow]")
    
    # Generate clean name for paths (e.g., 'Virtual-Mouse')
    repo_name = repo_url.rstrip("/").split("/")[-1].replace(".git", "")
    repo_index_path = os.path.join("data", "vectors", repo_name)
    
    vector_store = None
    embedder = None

    # --- 2. INDEX LOADING LOGIC ---
    if os.path.exists(repo_index_path):
        use_existing = Prompt.ask(
            f"Index for [green]{repo_name}[/green] found. Use existing index?", 
            choices=["y", "n"], 
            default="y"
        )
        if use_existing == "y":
            with console.status("[bold blue]Loading vector engine...[/bold blue]"):
                embedder = Embedder()
                vector_store = VectorStore.load(repo_name)
            
            # Load metadata if available
            meta = RepoMetadata.load(repo_index_path)
            if meta:
                # Accessing dictionary keys safely via .get()
                stats = meta.get('stats', {})
                console.print(f"[dim]Total Chunks: {stats.get('total_chunks', 'N/A')} | "
                              f"Files: {stats.get('total_files', 'N/A')}[/dim]")
        else:
            vector_store = run_ingestion(repo_url)
            embedder = Embedder()
    else:
        # No existing index found, start full ingestion
        vector_store = run_ingestion(repo_url)
        embedder = Embedder()

    # Final safety check to ensure engine is ready
    if not vector_store or not embedder:
        console.print("[bold red]Failed to initialize the codebase engine. Exiting.[/bold red]")
        return

    # --- 3. CHAT INTERFACE ---
    chat_ui = CLIChat()
    chat_ui.display_header(repo_name)
    feedback_service = FeedbackCollector()
    
    while True:
        try:
            query = Prompt.ask("\n[bold cyan]Query[/bold cyan]")
            
            if query.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if not query.strip():
                continue

            # Execute Query (Reranking + Groq)
            # This triggers the streaming response in the terminal
            answer_text = run_query(query, vector_store, embedder)
            
            # --- 4. FEEDBACK & LEARNING LOOP ---
            console.print("\n" + "─" * 60)
            feedback = Prompt.ask(
                "[italic white]Was this answer helpful?[/italic white]", 
                choices=["y", "n"], 
                default="y"
            )
            
            rating = 1 if feedback == "y" else 0
            # Save the query/answer pair to help the RankingOptimizer learn
            feedback_service.save_feedback(query, answer_text, rating)

        except KeyboardInterrupt:
            console.print("\n[yellow]Session ended by user. Exiting...[/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]System Error:[/bold red] {e}")

if __name__ == "__main__":
    main()