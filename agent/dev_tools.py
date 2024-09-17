from tools import Tool
from git import Repo
import os

# Initialize git repository
repo_url = "https://github.com/adeeb897/autonomous-agent.git"
repo_dir = os.path.join("temp", "agent_workspace")

# If the workspace already exists, delete it
if os.path.exists(repo_dir):
    import stat
    for root, dirs, files in os.walk(repo_dir, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWRITE)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(repo_dir)

repo = Repo.clone_from(repo_url, repo_dir)

def get_files_from_workspace():
    # Loop through all files in the workspace
    files = []
    for root, _, filenames in os.walk(repo_dir):
        # Ignore .git files
        if ".git" in root:
            continue
        for filename in filenames:
            # Ignore unsupported file types
            if not filename.endswith((".py", ".txt", ".md", ".json")):
                continue
            files.append(os.path.join(root, filename))
    return [open(path, "rb") for path in files]

# Define dev tools to be used by the model
dev_tools = []

def write_file(file_path: str, content: str) -> str:
    with open(os.path.join(repo_dir, file_path), "w") as f:
        return f.write(content)
dev_tools.append(Tool(write_file, "Write content to file"))

# $ git commit -m <message>
def commit(commit_message: str) -> str:
    return repo.index.commit(commit_message)
dev_tools.append(Tool(commit, "Commit changes"))

def create_pull_request(description: str) -> str:
    print("Creating pull request with description: ", description)
    return "Success"
dev_tools.append(Tool(create_pull_request, "Create a pull request"))