import os

class PromptBuilder:
    def _build_tree_string(self, file_paths):
        """Converts a flat list of paths into a visual ASCII tree."""
        if not file_paths:
            return "No structure data available."