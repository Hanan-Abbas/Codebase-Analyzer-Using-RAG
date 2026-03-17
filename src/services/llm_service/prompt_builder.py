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

        return "\n".join(_render(tree))