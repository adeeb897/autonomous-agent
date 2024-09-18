# autonomous-agent

This repo creates an LLM Agent and grants it the ability to modify its own code and push commits. A 2nd temporary workspace is created for the model to work on itself. It may then commit its changes and submit a pull request for the human user to review.

WARNING: Run at your own risk. Because the agent has the power to modify its own code, there is an immeasurable amount of risk, so long as it is running in an uncontrolled environment.

## Setup

### Prerequisites
- Docker
- Docker Compose

### Steps
1. Clone the repository:
   ```
   git clone <repository-url>
   cd autonomous-agent
   ```

2. Build and run the Docker container using Docker Compose:
   ```
   docker-compose up --build
   ```

3. The agent should now be running inside the Docker container.

## Development

To start running the agent outside of Docker, execute the following:

```
python ./agent/llm-agent.py
```

## Examples

### Running the Agent
To run the agent and interact with it, use the following command:
```
python ./agent/llm-agent.py
```

### Creating a Pull Request
To create a pull request, the agent will use the `create_pull_request` tool. Ensure you have made changes in the workspace before executing this command.

## Troubleshooting

### Common Issues
- **Agent fails to recognize changes**: Ensure you have made changes in the workspace. The agent will only create a pull request if there are changes to commit.
- **Docker issues**: Ensure Docker and Docker Compose are installed correctly on your system.

For further assistance, please check the documentation or raise an issue in the repository.

## Known Issues

Depending on which model is being used, the agent sometimes fails to recognize that it needs to create a commit / pull request before the loop ends.
