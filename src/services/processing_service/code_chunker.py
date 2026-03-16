from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

class CodeChunker:
    def __init__(self, extension):
        self.language = self._map_extension_to_language(extension)
        self.splitter = RecursiveCharacterTextSplitter.from_language(
            language=self.language,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )