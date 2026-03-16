import os
from git import Repo
from config.settings import REPO_STORAGE

class RepoCloner:
    def __init__(self, repo_url):
        self.repo_url = repo_url
        self.repo_name = repo_url.split("/")[-1].replace(".git", "")
        self.target_path = REPO_STORAGE / self.repo_name