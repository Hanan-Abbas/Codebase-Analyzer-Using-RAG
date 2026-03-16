import os
import json

def generate_repo_structure(repo_path):
    structure = []
    for root, dirs, files in os.walk(repo_path):
        # Ignore hidden folders like .git
        if '.git' in dirs: dirs.remove('.git')
        
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), repo_path)
            structure.append(relative_path)
    
    return structure