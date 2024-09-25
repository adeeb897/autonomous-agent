"""A module to manage a Git repository and create pull requests on GitHub."""

import time
from datetime import datetime, timezone
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

    def __init__(self, repo_dir, dry_run=False):
        self.dry_run = dry_run
        try:
            self.repo = Repo.clone_from(REPO_URL, repo_dir)
            # Initialize GitHub API using the access token environment variable
            self.github = Github(getenv(GITHUB_TOKEN_VAR))
            self.branch_name = None
            self.current_pr = None
        except GitCommandError as e:
            raise RuntimeError(f"Failed to initialize Git repository: {e}") from e
        except GithubException as e:
            raise RuntimeError(f"Failed to authenticate with GitHub: {e}") from e

    def create_pull_request(
        self,
        commit_message: str,
        pr_title: str,
        pr_description: str,
        user_prompt: str = None,
    ) -> str:
        """Create a pull request on GitHub with the given description and send it for review."""
        time_updated = datetime.now(timezone.utc)

        # If there are no unstaged changes or untracked files, return an error message
        if not self.repo.is_dirty() and not self.repo.untracked_files:
            return (
                "No changes to commit! "
                + "Please make some changes to the code using write_tool and try again."
            )

        # Create a temporary feature branch if one does not already exist
        if self.current_pr is None:
            self.branch_name = f"{BRANCH_NAME_PREFIX}-{int(time_updated.timestamp())}"
            self.repo.git.checkout("HEAD", b=self.branch_name)

        try:
            # Add, commit, and push all changes to the feature branch
            self.repo.git.add(all=True)
            self.repo.index.commit(f"{AI_GEN_PREFIX} {commit_message}")
            self.repo.remote(name="origin").push(self.branch_name)
        except GitCommandError as e:
            raise RuntimeError(f"Failed during git operations: {e}") from e

        try:
            if self.dry_run:
                print("Dry run mode enabled. Skipping pull request creation.")
                return "Dry run mode enabled. Skipping pull request creation."

            # Create a pull request if one does not already exist
            if self.current_pr is None:
                u_p = (
                    f' The user prompt for this change was: "{user_prompt}"\n'
                    if user_prompt and user_prompt != ""
                    else ""
                )
                repo = self.github.get_repo(REPO_NAME)
                self.current_pr = repo.create_pull(
                    title=f"{AI_GEN_PREFIX} {pr_title}",
                    body=f"{AI_GEN_PREFIX}{u_p}\n {pr_description}",
                    head=self.branch_name,
                    base="main",
                )
                print(f"Pull request created: {self.current_pr.html_url}")

            # Wait for the pull request to be reviewed and/or merged
            while True:
                print("Checking pull request status...")
                self.current_pr.update()
                # If the pull request is merged, return a success message
                if self.current_pr.merged:
                    print("Pull request has been merged!")
                    return "Pull request has been merged! Feel free to exit for now."
                # If the pull request is closed without being merged, return a failure message
                if self.current_pr.state == "closed":
                    self.current_pr = None
                    print("Pull request has been closed without being merged.")
                    return "Pull request has been closed. Please await further user instructions."
                # If comments are added, return them to the agent
                comments = self.current_pr.get_comments(
                    sort="added",
                    direction="desc",
                    since=time_updated,
                )
                if comments.totalCount > 0:
                    comment_block = ""
                    for comment in comments:
                        print(f'\nComment by {comment.user.login}: "{comment.body}"')
                        comment_block += (f"Comment by {comment.user.login} " +
                            f"(id={comment.id}, " +
                            f"path={comment.path}, " +
                            f"position={comment.position}): " +
                            f'"{comment.body}"\n')
                    return ("The below comments were received. " +
                        "Please reply with the respond_to_pr_comment tool.\n" +
                        comment_block)
                time.sleep(10)

        except GithubException as e:
            raise RuntimeError(f"Failed to create a pull request: {e}") from e

    def respond_to_pr_comment(self, comment_id: str, response: str) -> str:
        """Respond to a comment on the current pull request."""
        if self.current_pr is None:
            return (
                "No pull request is currently open. Please create a pull request first."
            )
        try:
            print(f"Responding to comment {comment_id} with: {response}")
            # Get comment object from the comment ID
            all_comments = self.current_pr.get_comments()
            top_level_comment = None
            comment_id_int = int(comment_id)
            for comment in all_comments:
                if comment.id == comment_id_int:
                    top_level_comment = comment
                    break
            if top_level_comment is None:
                return "Failed to find the comment with the given ID."
            commit = None
            for c in self.current_pr.get_commits():
                if c.sha == top_level_comment.commit_id:
                    commit = c
                    break
            if commit is None:
                return "Failed to find the commit associated with the comment."
            self.current_pr.create_comment(
                f"{AI_GEN_PREFIX} {response}",
                commit,
                top_level_comment.path,
                top_level_comment.position,
            )
            return "Response sent successfully."
        except GithubException as e:
            raise RuntimeError(f"Failed to respond to the comment: {e}") from e

    def list_recent_commits(self, num_of_commits: int) -> str:
        """List the recent commits on the feature branch."""
        commits = list(self.repo.iter_commits(self.branch_name))[:num_of_commits]
        return "\n".join(
            [f"{commit.hexsha[:5]}: {commit.message}" for commit in commits]
        )
