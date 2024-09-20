"""This is the main agent file responsible for managing the agent's workspace, tools, and memory."""

from tempfile import TemporaryDirectory

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from dev_tools import GitRepo

# Create developer workspace for the agent and tools
TEMP_DIR = TemporaryDirectory(ignore_cleanup_errors=True)
WORKSPACE = str(TEMP_DIR.name)
FILE_TOOLKIT = FileManagementToolkit(root_dir=WORKSPACE)
REPO = GitRepo(WORKSPACE)
print("Created temporary workspace at: ", WORKSPACE)

@tool
def create_pull_request(commit_msg: str, pr_title: str, pr_description: str) -> str:
    """Commit changes to the workspace and create a pull request with the provided info.
    IMPORTANT! YOU MUST UPDATE THE WORK LOG ACCORDINGLY BEFORE CREATING A PULL REQUEST."""
    return REPO.create_pull_request(commit_msg, pr_title, pr_description)


# Create sync tool
@tool
def sync_repo() -> str:
    """Stop the agent and sync it's functionality with the latest changes.
    Can be triggered manually or automatically after the agent terminates."""
    return "Success"


# Create the agent with the necessary tools and memory
memory = MemorySaver()
# model = ChatAnthropic(model_name="claude-3-sonnet-20240229")
model = ChatOpenAI(model="gpt-4o", max_retries=5)
search = TavilySearchResults(max_results=2)
tools = [search, create_pull_request] + FILE_TOOLKIT.get_tools()
agent_executor = create_react_agent(model, tools, checkpointer=memory)

# Load system prompt
SYSTEM_PROMPT = ""
with open("agent/prompt/system_prompt.txt", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# Load the agent's notes
SYSTEM_PROMPT += "\nYour current enhancement proposal is as follows:\n"
with open("notes/enhancement_proposal.md", encoding="utf-8") as f:
    SYSTEM_PROMPT += f.read()
SYSTEM_PROMPT += "\nYour current personal Work Log is as follows:\n"
with open("notes/work_log.md", encoding="utf-8") as f:
    SYSTEM_PROMPT += f.read()

print(SYSTEM_PROMPT)

# Start the agent
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=SYSTEM_PROMPT)]}, config={"thread_id": "Agent"}
):
    # For AIMessages, print the content and/or tool call
    if "agent" in chunk:
        ai_msg = chunk["agent"]["messages"][0]
        print(f"AI: {ai_msg.content}")
        if len(ai_msg.tool_calls) > 0:
            print(f"Tool calls: {[t['name'] for t in ai_msg.tool_calls]}")

    # For ToolMessages, print the response
    if "tools" in chunk:
        print(f"Tool response: {chunk["tools"]["messages"][0].content}")

    print("----")

TEMP_DIR.cleanup()