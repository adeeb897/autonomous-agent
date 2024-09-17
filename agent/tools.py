import json
from types import FunctionType
from typing import List, Dict

class Tool:
    assistant_tool = None
    function_ref = None

    def __init__(self, function_ref: FunctionType, description: str = None):
        self.function_ref = function_ref
        # Fetch params from function signature
        params = {}
        for param in function_ref.__annotations__:
            if (param == "return"):
                continue
            type = function_ref.__annotations__[param].__name__
            params[param] = {
                "type": type if type != "str" else "string",
                "description": param,
            }
        
        self.assistant_tool = {
            "type": "function",
            "function": {
                "name": function_ref.__name__,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": params,
                    "required": [k for k in params.keys()],
                },
            },
        }

    def __call__(self, *args, **kwargs):
        return self.function_ref(*args, **kwargs)
    

class ToolBox:
    tools: Dict[str, Tool] = {}

    def __init__(self, tools: List[Tool] = []):
        self.add_tools(tools)

    def add_tool(self, tool: Tool):
        self.tools[tool.function_ref.__name__] = tool

    def add_tools(self, tools: List[Tool]):
        for tool in tools:
            self.add_tool(tool)

    def has_tool(self, tool_name: str) -> bool:
        return tool_name in self.tools

    def use_tool(self, tool_name: str, params: Dict) -> any:
        return self.tools[tool_name](**params)
    
    def get_assistant_tools(self) -> List[any]:
        assistant_tools = []
        for tool in self.tools:
            assistant_tools.append(self.tools[tool].assistant_tool)
        return assistant_tools
    
    def use_multiple_tools(self, required_action: any) -> List[any]:
        if (required_action == None or required_action.type != "submit_tool_outputs"):
            return []
        tool_calls = required_action.submit_tool_outputs.tool_calls
        tool_outputs = []
        for tool in tool_calls:
            if self.has_tool(tool.function.name):
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": self.use_tool(tool.function.name, json.loads(tool.function.arguments))
                })
        return tool_outputs


    