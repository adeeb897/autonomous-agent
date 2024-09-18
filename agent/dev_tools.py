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
ai_gen_prefix = "[AI Generated]"

class GitRepo:
    
    def __init__(self, repo_dir):
        self.repo = Repo.clone_from(repo_url, repo_dir)
        # Initialize GitHub API using the access token environment variable
        self.github = Github(getenv(github_token_var))
        # Create a temporary feature branch
        self.repo.git.checkout("HEAD", b=branch_name)

    def create_pull_request(self, commit_message: str, pr_title: str, pr_description: str) -> str:
        """Create a pull request on GitHub with the given description and send it for review."""

        # If there are no unstaged changes, return an error message
        if not self.repo.is_dirty():
            return "No changes to commit! Please make some changes to the code using write_tool and try again."       

        # Add and commit all changes to the feature branch
        self.repo.git.add(all=True)
        self.repo.index.commit(f"{ai_gen_prefix} {commit_message}")

        origin = self.repo.remote(name='origin')
        origin.push(branch_name)

        # Create a pull request
        repo = self.github.get_repo(repo_name)
        pr = repo.create_pull(
            title=f"{ai_gen_prefix} {pr_title}",
            body=f"{ai_gen_prefix} {pr_description}",
            head=branch_name,
            base="main"
        )
        print(f"Pull request created: {pr.html_url}")
        return f"Pull request created: {pr.html_url}"