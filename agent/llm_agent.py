"""This is the main agent file responsible for managing the agent's workspace, tools, and memory."""

from tempfile import TemporaryDirectory
import argparse

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from dev_tools import GitRepo

# Parse command line arguments
parser = argparse.ArgumentParser(description="Launch the AI Agent.")
parser.add_argument("--dryrun",
                    action="store_true",
                    help="Run the agent in dryrun mode, i.e. don't actually create a pull request.",
                    default=False)
parser.add_argument("--user-prompt",
                    type=str,
                    help="Pass the provided user prompt to the agent.",
                    default=None)
args = parser.parse_args()


with TemporaryDirectory(ignore_cleanup_errors=True) as TEMP_DIR:
    # Create developer workspace for the agent and tools
    WORKSPACE = str(TEMP_DIR)
    FILE_TOOLKIT = FileManagementToolkit(root_dir=WORKSPACE)
    REPO = GitRepo(WORKSPACE, dry_run=args.dryrun)
    print("Created temporary workspace at: ", WORKSPACE)

    @tool
    def create_pull_request(commit_msg: str, pr_title: str, pr_description: str) -> str:
        """Commit changes to the workspace and create a pull request with the provided info.
        IMPORTANT! YOU MUST UPDATE THE WORK LOG ACCORDINGLY BEFORE CREATING A PULL REQUEST."""
        return REPO.create_pull_request(commit_msg, pr_title, pr_description, args.user_prompt)

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

    # Inject the agent's notes as needed
    while SYSTEM_PROMPT.find("{{") != -1:
        start = SYSTEM_PROMPT.find("{{")
        end = SYSTEM_PROMPT.find("}}", start)
        file_path = SYSTEM_PROMPT[start+2:end]
        with open(file_path, encoding="utf-8") as f:
            SYSTEM_PROMPT = SYSTEM_PROMPT[:start] + f.read() + SYSTEM_PROMPT[end+2:]

    if args.user_prompt and args.user_prompt != "":
        SYSTEM_PROMPT += f"\nThe user prompt is: {args.user_prompt}\n"

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
