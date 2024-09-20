import time

class GitRepo:
    """A class to manage a Git repository and create pull requests on GitHub."""

    def __init__(self, repo_dir, dry_run=False):
        self.dry_run = dry_run
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
        self, commit_message: str, pr_title: str, pr_description: str, user_prompt: str = None
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
            if self.dry_run:
                print("Dry run mode enabled. Skipping pull request creation.")
                return "Dry run mode enabled. Skipping pull request creation."
            u_p = f" The user prompt for this change was: \"{user_prompt}\"" if user_prompt and user_prompt != "" else ""
            # Create a pull request
            repo = self.github.get_repo(REPO_NAME)
            pr = repo.create_pull(
                title=f"{AI_GEN_PREFIX} {pr_title}",
                body=f"{AI_GEN_PREFIX}{u_p}\n {pr_description}",
                head=self.branch_name,
                base="main",
            )
            print(f"Pull request created: {pr.html_url}")

            # Loop to check for comments or PR merge
            while True:
                pr.update()
                if pr.merged:
                    print("Pull request has been merged.")
                    return "Pull request has been merged."
                comments = pr.get_issue_comments()
                for comment in comments:
                    print(f"Comment by {comment.user.login}: {comment.body}")
                    return f"Comment by {comment.user.login}: {comment.body}"
                time.sleep(30)  # Wait for 30 seconds before checking again

        except GithubException as e:
            raise RuntimeError(f"Failed to create a pull request: {e}") from e

    def list_recent_commits(self, num_of_commits: int) -> str:
        """List the recent commits on the feature branch."""
        commits = list(self.repo.iter_commits(self.branch_name))[:num_of_commits]
        return "\n".join(
            [f"{commit.hexsha[:5]}: {commit.message}" for commit in commits]
        )
