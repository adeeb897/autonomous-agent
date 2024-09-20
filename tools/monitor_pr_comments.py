import requests

# Function to get comments on a specific PR

def get_pr_comments(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Example usage
if __name__ == "__main__":
    repo = "user/repo_name"  # Update with actual repo name
    pr_number = 1  # Update with actual PR number
    token = "your_github_token"  # Update with actual GitHub token
    comments = get_pr_comments(repo, pr_number, token)
    for comment in comments:
        print(comment)