# autonomous-agent

This repo creates an LLM Agent and grants it the ability to modify its own code and push commits. A 2nd temporary workspace is created for the model to work on itself. It may then commit its changes and submit a pull request for the human user to review.

WARNING: Run at your own risk. Because the agent has the power to modify its own code, there is an immeasurable amount of risk, so long as it is running in an uncontrolled environment.

TODO: Isolate the agent to a sandboxed environment.


## Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Docker (optional, for sandboxing)

### Instructions

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/autonomous-agent.git
   cd autonomous-agent
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```
   pip install -r requirements.txt
   ```

4. **Set up Docker** (if using sandboxing):
   - Install Docker from [Docker's official website](https://www.docker.com/get-started).
   - Ensure Docker is running.

## Development

To start running the agent execute the following:

```
python ./agent/llm_agent.py
```

## Enhancements and Proposals

### 1. Implement a Sandboxed Environment
- **Objective**: Ensure the agent operates within controlled confines to prevent unintended actions.
- **Steps**:
  - Research Docker and other containerization tools.
  - Implement a sandboxing technique suitable for the agent’s operations.
  - Test the sandboxed environment to ensure it isolates the agent effectively.

### 2. Develop the Knowledge Ingestion Pipeline
- **Objective**: Automate the process of fetching, filtering, and ingesting educational resources.
- **Steps**:
  - Identify and evaluate trusted educational sources.
  - Create tools to fetch and preprocess these resources.
  - Implement automated content filtering (toxicity analysis, bias detection).

### 3. Enable Safe Knowledge Querying
- **Objective**: Allow the agent to query the expanded knowledge base safely.
- **Steps**:
  - Develop mechanisms for read-only queries.
  - Ensure separation from the underlying model weights.
  - Test the querying mechanisms for safety and reliability.

### 4. Strengthen Ethical and Safety Checks
- **Objective**: Ensure all processes align with ethical guidelines and safety constraints.
- **Steps**:
  - Integrate ethical checks throughout the knowledge ingestion and querying processes.
  - Regularly test and validate these checks.
  - Update ethical guidelines as necessary.

### 5. Establish Regular Human Oversight
- **Objective**: Maintain human oversight to review significant changes and new integrations.
- **Steps**:
  - Generate usage examples from the new knowledge base.
  - Submit these examples for human review.
  - Use the pull request workflow for approval.

## Known Issues

Depending on which model is being used, the agent sometimes fails to recognize that it needs to create a commit / pull request before the loop ends.

## Examples

### Running the Agent
To start the agent, run:
```
python ./agent/llm_agent.py
```

### Common Usage Scenarios
- **Modifying Code**: The agent can propose code changes and create pull requests for review.
- **File Management**: The agent can read, write, move, and delete files within its workspace.
- **Web Search**: The agent can perform web searches to gather information.

## Troubleshooting

### Common Issues

1. **Installation Problems**:
   - Ensure all prerequisites are installed and correctly configured.
   - Verify the virtual environment is activated if used.

2. **Docker Issues**:
   - Ensure Docker is installed and running if sandboxing is enabled.
   - Check Docker's documentation for common troubleshooting tips.

3. **Agent Errors**:
   - Review the error messages for clues.
   - Ensure the agent has the necessary permissions to perform actions.
   - Check network connectivity if the agent relies on external resources.

For further assistance, please open an issue on the [GitHub repository](https://github.com/yourusername/autonomous-agent/issues).
