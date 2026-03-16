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

    def _map_extension_to_language(self, ext):
        mapping = {
            '.py': Language.PYTHON,
            '.js': Language.JS,
            '.ts': Language.TS,
            '.cpp': Language.CPP,
            '.java': Language.JAVA,
        }
        return mapping.get(ext, Language.MARKDOWN)

    def chunk_text(self, text, metadata):
        chunks = self.splitter.create_documents([text], metadatas=[metadata])
        for chunk in chunks:
            # Prepend file path to content for "Deep Awareness"
            chunk.page_content = f"FILE: {metadata['file_path']}\n{chunk.page_content}"
        return chunks