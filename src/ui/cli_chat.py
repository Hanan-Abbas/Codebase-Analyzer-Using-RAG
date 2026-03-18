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

    def stream_response(self, text_gen):
        """
        Displays the response in real-time as it arrives from Groq.
        """
        full_text = ""
        with Live(Markdown(""), refresh_per_second=10, console=self.console) as live:
            for chunk in text_gen:
                full_text += chunk
                live.update(Markdown(full_text))
        return full_text

    def show_error(self, message):
        self.console.print(f"[bold red]Error:[/bold red] {message}")