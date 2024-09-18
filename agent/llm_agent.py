from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from tempfile import TemporaryDirectory
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain.tools import tool
from dev_tools import GitRepo

class Agent:
    def __init__(self):
        self.working_directory = TemporaryDirectory()
        self.root_dir = str(self.working_directory.name)
        self.file_toolkit = FileManagementToolkit(root_dir=self.root_dir)
        self.repo = GitRepo(self.root_dir)
        self.memory = MemorySaver()
        self.model = ChatOpenAI(model="gpt-4o", max_retries=5)
        self.search = TavilySearchResults(max_results=2)
        self.tools = [self.search, self.create_pull_request] + self.file_toolkit.get_tools()
        self.agent_executor = create_react_agent(self.model, self.tools, checkpointer=self.memory)

    @tool
    def create_pull_request(self, commit_msg: str, pr_title: str, pr_description: str) -> str:
        return self.repo.create_pull_request(commit_msg, pr_title, pr_description)

    @tool
    def sync_repo(self) -> str:
        return "Success"

    def load_system_prompt(self) -> str:
        system_prompt = ""
        with open("agent/prompt/system_prompt.txt") as f:
            system_prompt = f.read()
        system_prompt += "\nYou currently have the following plan stored within plan.txt:\n"
        with open("plan.txt") as f:
            system_prompt += f.read()
        system_prompt += "\n\nRecent commits:\n"
        system_prompt += self.repo.list_recent_commits(5)
        return system_prompt

    def start_agent(self):
        system_prompt = self.load_system_prompt()
        for chunk in self.agent_executor.stream(
            {"messages": [HumanMessage(content=system_prompt)]}, config={"thread_id": "Agent"}
        ):
            print(chunk)
            print("----")

if __name__ == '__main__':
    agent = Agent()
    agent.start_agent()
