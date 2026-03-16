import os
from git import Repo
from config.settings import REPO_STORAGE

class RepoCloner:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.repo_name = repo_url.split("/")[-1].replace(".git", "")
        self.target_path = REPO_STORAGE / self.repo_name

    def clone(self):
        if self.target_path.exists():
            print(f"Directory {self.repo_name} already exists. Skipping clone.")
            return self.target_path
        
        print(f"Cloning {self.repo_url} into {self.target_path}...")
        try:
            Repo.clone_from(self.repo_url, self.target_path)
            print("Clone successful!")
            return self.target_path
        except Exception as e:
            print(f"Error during cloning: {e}")
            return None