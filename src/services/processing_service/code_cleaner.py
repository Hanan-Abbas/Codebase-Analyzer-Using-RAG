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