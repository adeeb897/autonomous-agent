# from tools import Tool
from git import Repo
from github import Github
from langchain.tools import tool
from os import getenv

# Configure git repository
repo_name = "adeeb897/autonomous-agent"
repo_url = f"https://github.com/{repo_name}.git"
branch_name = "feature_branch"
github_token_var = "GITHUB_ACCESS_TOKEN"

class GitRepo:
    
    def __init__(self, repo_dir):
        self.repo = Repo.clone_from(repo_url, repo_dir)
        # Initialize GitHub API using the access token environment variable
        self.github = Github(getenv(github_token_var))
        # Create a temporary feature branch
        self.repo.git.checkout("HEAD", b=branch_name)

    # $ git commit -m <message>
    @tool
    def commit(self, commit_message: str) -> str:
        """Commit changes to the git repository with the given commit message."""
        return self.repo.index.commit(commit_message)

    @tool
    def create_pull_request(self, description: str) -> str:
        """Create a pull request on GitHub with the given description and send it for review."""
        origin = self.repo.remote(name='origin')
        origin.push(branch_name)

        # Create a pull request
        repo = self.github.get_repo(self.repo_name)
        pr = repo.create_pull(
            title="Pull request from " + branch_name,
            body=description,
            head=branch_name,
            base="main"
        )
        print(f"Pull request created: {pr.html_url}")
        return f"Pull request created: {pr.html_url}"