"""A module to manage a Git repository and create pull requests on GitHub."""

from os import getenv
from git import Repo, GitCommandError
from github import Github, GithubException

# Configure git repository
REPO_NAME = "adeeb897/autonomous-agent"
REPO_URL = f"https://github.com/{REPO_NAME}.git"
BRANCH_NAME_PREFIX = "feature-branch"
GITHUB_TOKEN_VAR = "GITHUB_ACCESS_TOKEN"
AI_GEN_PREFIX = "[AI Generated]"

class GitRepo:
    """A class to manage a Git repository and create pull requests on GitHub."""

    def __init__(self, repo_dir):
        try:
            self.repo = Repo.clone_from(REPO_URL, repo_dir)
            # Initialize GitHub API using the access token environment variable
            self.github = Github(getenv(GITHUB_TOKEN_VAR))
            # Create a temporary feature branch
            self.branch_name = (
                f"{BRANCH_NAME_PREFIX}-{self.repo.head.commit.hexsha[:7]}"
            )
            self.repo.git.checkout("HEAD", b=self.branch_name)
        except GitCommandError as e:
            raise RuntimeError(f"Failed to initialize Git repository: {e}") from e
        except GithubException as e:
            raise RuntimeError(f"Failed to authenticate with GitHub: {e}") from e

    def create_pull_request(
        self, commit_message: str, pr_title: str, pr_description: str
    ) -> str:
        """Create a pull request on GitHub with the given description and send it for review."""

        # If there are no unstaged changes or untracked files, return an error message
        if not self.repo.is_dirty() and not self.repo.untracked_files:
            return (
                "No changes to commit! "
                + "Please make some changes to the code using write_tool and try again."
            )

        try:
            # Add, commit, and push all changes to the feature branch
            self.repo.git.add(all=True)
            self.repo.index.commit(f"{AI_GEN_PREFIX} {commit_message}")
            self.repo.remote(name="origin").push(self.branch_name)
        except GitCommandError as e:
            raise RuntimeError(f"Failed during git operations: {e}") from e

        try:
            # Create a pull request
            repo = self.github.get_repo(REPO_NAME)
            pr = repo.create_pull(
                title=f"{AI_GEN_PREFIX} {pr_title}",
                body=f"{AI_GEN_PREFIX}\n {pr_description}",
                head=self.branch_name,
                base="main",
            )
            print(f"Pull request created: {pr.html_url}")
            return pr
        except GithubException as e:
            raise RuntimeError(f"Failed to create a pull request: {e}") from e

    def list_recent_commits(self, num_of_commits: int) -> str:
        """List the recent commits on the feature branch."""
        commits = list(self.repo.iter_commits(self.branch_name))[:num_of_commits]
        return "\n".join(
            [f"{commit.hexsha[:5]}: {commit.message}" for commit in commits]
        )
