# Import relevant functionality
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from tempfile import TemporaryDirectory
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain.tools import tool
from dev_tools import GitRepo

# Create developer workspace for the agent and tools
working_directory = TemporaryDirectory()
root_dir = str(working_directory.name)
file_toolkit = FileManagementToolkit(root_dir=root_dir)
repo = GitRepo(root_dir)
print("Created temporary workspace at: ", root_dir)

@tool
def create_pull_request(commit_msg: str, pr_title: str, pr_description: str) -> str:
    """Commit changes to the workspace and create a GitHub pull request with the provided title/description."""
    return repo.create_pull_request(commit_msg, pr_title, pr_description)


# Create sync tool
@tool
def sync_repo() -> str:
    """Stop the agent and sync it's functionality with the latest changes. Can be triggered manually or automatically after the agent terminates."""
    return "Success"


# Create the agent with the necessary tools and memory
memory = MemorySaver()
# model = ChatAnthropic(model_name="claude-3-sonnet-20240229")
model = ChatOpenAI(model="gpt-4o", max_retries=5)
search = TavilySearchResults(max_results=2)
tools = [search, create_pull_request] + file_toolkit.get_tools()
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Load system prompt
system_prompt = ""
with open("agent/prompt/system_prompt.txt") as f:
    system_prompt = f.read()

# Load the agent's stored plan
system_prompt += "\nYou currently have the following plan stored within plan.txt:\n"
with open("plan.txt") as f:
    system_prompt += f.read()

# Append recent commits to the system prompt
system_prompt += "\n\nRecent commits:\n"
system_prompt += repo.list_recent_commits(5)

print(system_prompt)

# Start the agent
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=system_prompt)]}, config={"thread_id": "Agent"}
):
    print(chunk)
    print("----")
