# from tools import Tool
from git import Repo
from github import Github
from langchain.tools import tool
from os import getenv

# Configure git repository
repo_name = "adeeb897/autonomous-agent"
repo_url = f"https://github.com/{repo_name}.git"
branch_name_prefix = "feature-branch"
github_token_var = "GITHUB_ACCESS_TOKEN"
ai_gen_prefix = "[AI Generated]"

class GitRepo:
    
    def __init__(self, repo_dir):
        self.repo = Repo.clone_from(repo_url, repo_dir)
        # Initialize GitHub API using the access token environment variable
        self.github = Github(getenv(github_token_var))
        # Create a temporary feature branch
        self.branch_name = f"{branch_name_prefix}-{self.repo.head.commit.hexsha[:7]}"
        self.repo.git.checkout("HEAD", b=self.branch_name)

    def create_pull_request(self, commit_message: str, pr_title: str, pr_description: str) -> str:
        """Create a pull request on GitHub with the given description and send it for review."""

        # If there are no unstaged changes or untracked files, return an error message
        if not self.repo.is_dirty() and not self.repo.untracked_files:
            return "No changes to commit! Please make some changes to the code using write_tool and try again."       

        # Add, commit, and push all changes to the feature branch
        self.repo.git.add(all=True)
        self.repo.index.commit(f"{ai_gen_prefix} {commit_message}")
        self.repo.remote(name='origin').push(self.branch_name)

        # Create a pull request
        repo = self.github.get_repo(repo_name)
        pr = repo.create_pull(
            title=f"{ai_gen_prefix} {pr_title}",
            body=f"{ai_gen_prefix} {pr_description}",
            head=self.branch_name,
            base="main"
        )
        print(f"Pull request created: {pr.html_url}")
        return pr

    def list_recent_commits(self, num_of_commits: int) -> str:
        """List the recent commits on the feature branch."""
        commits = list(self.repo.iter_commits(self.branch_name))[:num_of_commits]
        return "\n".join([f"{commit.hexsha[:5]}: {commit.message}" for commit in commits])