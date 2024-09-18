# autonomous-agent

This repo creates an LLM Agent and grants it the ability to modify it's own code and push commits. A 2nd temporary workspace is created for the model to work on itself. It may then commit it's changes and submit a pull request for the human user to review.

WARNING: Run at your own risk. Because the agent has the power to modify it's own code, there is an immeasurable amount of risk, so long as it is running in an uncontrolled environment.

TODO: Isolate the agent to a sandboxed environment.


## Setup

TODO


## Development

To start running the agent execute the following:

```
python ./agent/llm-agent.py
```

## Known Issues

Depending on which model is being used, the agent sometimes fails to recognize that it needs to create a commit / pull request before the loop ends.