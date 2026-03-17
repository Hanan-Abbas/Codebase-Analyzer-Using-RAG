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

        def _render(node, prefix=""):
            lines = []
            items = sorted(node.items())
            for i, (name, children) in enumerate(items):
                is_last = (i == len(items) - 1)
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{name}")
                if children:
                    extension = "    " if is_last else "│   "
                    lines.extend(_render(children, prefix + extension))
            return lines

        return "\n".join(_render(tree))def build_code_qa_prompt(self, query, context_docs, physical_files=None):
        # Generate the visual tree hierarchy
        repo_tree = self._build_tree_string(physical_files)
        
        # Format the code chunks
        code_context = "\n\n".join([
            f"--- SOURCE: {d.metadata.get('file_path', 'Unknown')} ---\n{d.page_content}" 
            for d in context_docs
        ])

        return f"""You are RepoMind, an AI Code Expert with high-level Repository Authority.