import os

class PromptBuilder:
    def _build_tree_string(self, file_paths):
        """Converts a flat list of paths into a visual ASCII tree."""
        if not file_paths:
            return "No structure data available."
        
        tree = {}
        for path in file_paths:
            # Handle both forward and backward slashes for cross-platform support
            parts = path.replace("\\", "/").strip("/").split("/")
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

    def build_code_qa_prompt(self, query, context_docs, physical_files=None):
        """Generates the final prompt for the LLM with tree hierarchy and code context."""
        # Generate the visual tree hierarchy
        repo_tree = self._build_tree_string(physical_files)
        
        # Format the code chunks with clear source headers
        code_context = "\n\n".join([
            f"--- SOURCE: {d.metadata.get('file_path', 'Unknown')} ---\n{d.page_content}" 
            for d in context_docs
        ])

        return f"""You are RepoMind, an AI Code Expert with high-level Repository Authority.
        
[GROUND TRUTH: DIRECTORY HIERARCHY]
Below is the verified structure of the repository. Use this to understand module nesting and architecture:

{repo_tree}

[SEMANTIC CODE CONTEXT]
{code_context}

USER QUERY: {query}

STRICT INSTRUCTIONS:
1. Refer to the [DIRECTORY HIERARCHY] to understand where files are located.
2. If the user asks about architecture, use the tree structure to explain the relationships between directories.
3. Use Markdown: **Bold** for filenames, `code` for logic, and ### for sections.
4. If a file is mentioned in documentation but is missing from the [DIRECTORY HIERARCHY], flag it as a discrepancy."""