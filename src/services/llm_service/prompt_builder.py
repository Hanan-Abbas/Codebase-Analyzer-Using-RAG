import os

class PromptBuilder:
    def _build_tree_string(self, file_paths):
        """Converts a flat list of paths into a visual ASCII tree."""
        if not file_paths:
            return "No structure data available."
        
        tree = {}
        for path in file_paths:
            parts = path.strip("/").split("/")
            current = tree
            for part in parts:
                current = current.setdefault(part, {})