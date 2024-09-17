import os
from openai import AzureOpenAI
from dev_tools import dev_tools, get_files_from_workspace
from tools import ToolBox
import time

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

def run_requires_custom_tools(run):
    return run.status == "requires_action" and run.required_action and run.required_action.type == "submit_tool_outputs" and "search_files" not in [tc.function.name for tc in run.required_action.submit_tool_outputs.tool_calls]

# Load system prompt
with open("agent/prompt/system_prompt.txt") as f:
    system_prompt = f.read()
    print(system_prompt)

    # Setup git workspace for the agent and upload files to vector store
    files = get_files_from_workspace()
    vector_store = client.beta.vector_stores.create(name="Workspace")
    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=files
    )

    # Load functions as tools
    toolbox: ToolBox = ToolBox(dev_tools)

    # Create an assistant
    assistant = client.beta.assistants.create(
        name="Self-modifying AI agent",
        instructions=system_prompt,
        tools=toolbox.get_assistant_tools(),
        model="selfmodifyingagentdeployment-backup"
    )
    assistant = client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    # Create a thread
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="What would you like to do?"
    )

    # Run the initial pass
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    completed: bool = False

    # Loop until the model decides to exit
    start_time = time.time()
    while run.status not in ["completed", "cancelled", "expired", "failed"]:
        time.sleep(10)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
        print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
        print(f'Status: {run.status}')

        if run.status in ["cancelled", "expired", "failed"]:
            print("Run status: ", run.status)
            print(run.last_error)
            break
        elif run_requires_custom_tools(run):
            # Execute tools
            print("Tools: ", run.required_action)
            tool_outputs = toolbox.use_multiple_tools(run.required_action)

            # Submit a follow-up run
            if tool_outputs:
                try:
                    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tool_outputs
                    )
                    print("Tool outputs submitted successfully.")
                except Exception as e:
                    print("Failed to submit tool outputs:", e)
            else:
                print("No custom tool outputs to submit.")
                if run.status not in ["completed", "cancelled", "expired", "failed"]:
                    continue
                message = client.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content="No tool outputs were returned. What would you like to do next?"
                )
                run = client.beta.threads.runs.create(
                    thread_id=thread.id,
                    assistant_id=assistant.id,
                )

    print("\n\nFull thread:")
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print(messages.to_json(indent=2))