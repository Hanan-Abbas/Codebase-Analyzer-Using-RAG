from openai import OpenAI
from config.settings import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL
from rich.console import Console

console = Console()

class AnswerGenerator:
    def __init__(self):
        self.client = OpenAI(
            base_url=GROQ_BASE_URL,
            api_key=GROQ_API_KEY
        )

    def generate_answer(self, prompt):
        console.print(f"\n[bold magenta]RepoMind is querying Groq LPU ({LLM_MODEL})...[/bold magenta]\n")
        
        try:
            full_response = ""
            # Stream the response for a "live typing" feel
            stream = self.client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are an elite software architect."},
                    {"role": "user", "content": prompt}
                ],
                stream=True,
            )