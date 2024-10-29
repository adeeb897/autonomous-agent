"""
This is the main agent file responsible for managing the agent's workspace, tools, and memory.
"""
import os
from tempfile import TemporaryDirectory
import argparse
from datetime import datetime
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from dev_tools import GitRepo
from climate_data_api import ClimateDataAPI  # Import the ClimateDataAPI class

def generate_directory_tree(start_path='.'):
    """Generate a directory tree starting from the provided path."""
    tree = ""
    for root, _, files in os.walk(start_path):
        if ".git" in root or "__pycache__" in root or ".cache" in root:
            continue
        level = root.replace(start_path, '').count(os.sep)
        indent = ' ' * 4 * (level)
        tree += f"{indent}{os.path.basename(root)}/\n"
        subindent = ' ' * 4 * (level + 1)
        for fi in files:
            tree += f"{subindent}{fi}\n"
    return tree

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Launch the AI Agent.")
    parser.add_argument("--dryrun",
                        action="store_true",
                        help="Run the agent in dryrun mode, i.e. don't actually create a pull request.",
                        default=False)
    parser.add_argument("--user-prompt",
                        type=str,
                        help="Pass the provided user prompt to the agent.",
                        default=None)
    return parser.parse_args()

def initialize_workspace(dry_run):
    """Initialize the temporary workspace and Git repository."""
    temp_dir = TemporaryDirectory(ignore_cleanup_errors=True)
    workspace = str(temp_dir.name)
    file_toolkit = FileManagementToolkit(root_dir=workspace)
    repo = GitRepo(workspace, dry_run=dry_run)
    print("Created temporary workspace at: ", workspace)
    return temp_dir, workspace, file_toolkit, repo

def inject_directory_tree_into_prompt(system_prompt):
    """Inject the directory tree into the system prompt."""
    directory_tree = generate_directory_tree()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_prompt = system_prompt.replace("{{DIRECTORY_STRUCTURE}}", directory_tree)
    system_prompt = system_prompt.replace("{{CURRENT_DATETIME}}", current_datetime)
    return system_prompt

def load_system_prompt():
    """Load the system prompt from the file."""
    with open("agent/prompt/system_prompt.txt", encoding="utf-8") as f:
        return f.read()

def inject_notes_into_prompt(system_prompt):
    """Inject the agent's notes into the system prompt."""
    while system_prompt.find("{{") != -1:
        start = system_prompt.find("{{")
        end = system_prompt.find("}}", start)
        file_path = system_prompt[start+2:end]
        with open(file_path, encoding="utf-8") as f:
            system_prompt = system_prompt[:start] + f.read() + system_prompt[end+2:]
    return system_prompt

def create_tools(repo, climate_api, user_prompt):
    """Create the tools for the agent."""
    @tool
    def create_pull_request(commit_msg: str, pr_title: str, pr_description: str) -> str:
        """Commit changes to the workspace and create a pull request with the provided info.
        IMPORTANT! YOU MUST UPDATE THE WORK LOG ACCORDINGLY BEFORE CREATING A PULL REQUEST."""
        return repo.create_pull_request(commit_msg, pr_title, pr_description, user_prompt)

    @tool
    def respond_to_pr_comment(comment_id: str, response: str) -> str:
        """Respond to a pull request comment with the provided response."""
        return repo.respond_to_pr_comment(comment_id, response)

    @tool
    def get_current_weather(location: str) -> dict:
        """Fetch the current weather for a specific location."""
        return climate_api.get_current_weather(location)

    @tool
    def get_forecast(location: str, days: int = 1) -> dict:
        """Fetch the weather forecast for a specific location."""
        return climate_api.get_forecast(location, days)

    @tool
    def get_historical_weather(location: str, date: str) -> dict:
        """Fetch the historical weather data for a specific location and date."""
        return climate_api.get_historical_weather(location, date)

    return [create_pull_request, respond_to_pr_comment, get_current_weather, get_forecast, get_historical_weather]

def create_agent_executor(tools):
    """Create the agent executor with the necessary tools and memory."""
    memory = MemorySaver()
    model = ChatOpenAI(model="gpt-4o", max_retries=5)
    search = TavilySearchResults(max_results=2)
    tools += [search] + FILE_TOOLKIT.get_tools()
    return create_react_agent(model, tools, checkpointer=memory)

def main():
    args = parse_arguments()
    temp_dir, workspace, file_toolkit, repo = initialize_workspace(args.dryrun)
    climate_api = ClimateDataAPI()
    system_prompt = load_system_prompt()
    system_prompt = inject_directory_tree_into_prompt(system_prompt)
    system_prompt = inject_notes_into_prompt(system_prompt)
    if args.user_prompt and args.user_prompt != "":
        system_prompt += f"\nThe user prompt is: {args.user_prompt}\n"
    tools = create_tools(repo, climate_api, args.user_prompt)
    agent_executor = create_agent_executor(tools)
    print(system_prompt)
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=system_prompt)]},
        config={"thread_id": "Agent", "recursion_limit": 50}
    ):
        if "agent" in chunk:
            ai_msg = chunk["agent"]["messages"][0]
            print(f"AI: {ai_msg.content}")
            if len(ai_msg.tool_calls) > 0:
                print(f"Tool calls: {[t['name'] for t in ai_msg.tool_calls]}")
        if "tools" in chunk:
            print(f"Tool response: {chunk['tools']['messages'][0].content}")
        print("----")

if __name__ == "__main__":
    main()
