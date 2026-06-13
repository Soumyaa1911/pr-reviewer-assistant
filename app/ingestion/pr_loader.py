import requests
from app.core.config import settings


def get_pr_diff(repo_owner: str, repo_name: str, pr_number: int) -> str:
    """Fetch the diff for a given PR from GitHub."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.text