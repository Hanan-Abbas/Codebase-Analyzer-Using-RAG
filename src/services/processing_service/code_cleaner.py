import re

class CodeCleaner:
    @staticmethod
    def clean(content):
        """
        Basic cleaning to remove artifacts that confuse the embedding model.
        """
        if not content:
            return ""
        
        # Remove multiple newlines to save tokens
        content = re.sub(r'\n\s*\n', '\n\n', content)
        
        # Strip trailing whitespace from each line
        content = "\n".join([line.rstrip() for line in content.splitlines()])
        
        return content.strip()

    @staticmethod
    def is_likely_binary(content):
        """Check if a file is binary vs text."""
        text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
        return bool(content.translate(None, text_chars))