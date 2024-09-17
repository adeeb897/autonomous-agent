# Import relevant functionality
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from tempfile import TemporaryDirectory
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain.tools import tool
from dev_tools import GitRepo

# Create developer workspace for the agent
working_directory = TemporaryDirectory()
root_dir = str(working_directory.name)
file_toolkit = FileManagementToolkit(root_dir=root_dir)
repo = GitRepo(root_dir)
print("Created temporary workspace at: ", root_dir)


# Create sync tool
@tool
def sync_repo() -> str:
    """Stop the agent and sync it's functionality with the latest changes. Can be triggered manually or automatically after the agent terminates."""
    return "Success"


# Create the agent with the necessary tools and memory
memory = MemorySaver()
model = ChatAnthropic(model_name="claude-3-sonnet-20240229")
search = TavilySearchResults(max_results=2)
tools = [search, repo.commit, sync_repo] + file_toolkit.get_tools()
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Load system prompt
system_prompt = ""
with open("agent/prompt/system_prompt.txt") as f:
    system_prompt = f.read()
    print(system_prompt)

# Load the agent's stored plan
plan = "You currently have the following plan stored (within plan.txt):\n"
with open("plan.txt") as f:
    plan += f.read()
    print(plan)

# Start the agent
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=system_prompt)]}, config={"thread_id": "Agent"}
):
    print(chunk)
    print("----")
