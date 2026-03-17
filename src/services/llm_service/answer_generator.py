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