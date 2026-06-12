import os
import tempfile
from git import Repo


def clone_repo(repo_url: str) -> str:
    """Clone a GitHub repo into a temporary directory and return its path."""
    temp_dir = tempfile.mkdtemp()
    Repo.clone_from(repo_url, temp_dir)
    return temp_dir


def get_python_files(repo_path: str) -> list[str]:
    """Return a list of full paths to all .py files in the repo."""
    py_files = []
    for root, _, files in os.walk(repo_path):
        if ".git" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    return py_files