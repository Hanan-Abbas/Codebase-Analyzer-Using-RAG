from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.markdown import Markdown

class CLIChat:
    def __init__(self):
        self.console = Console()

    def display_header(self, repo_name):
        self.console.print(Panel(
            f"[bold green]Connected to: {repo_name}[/bold green]\n"
            "Ask technical questions or type 'exit' to quit.",
            title="RepoMind Chat Session",
            border_style="cyan"
        ))