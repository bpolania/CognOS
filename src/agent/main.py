#!/usr/bin/env python3
"""
CognOS Agent - AI Command Processing Core

This module handles natural language processing and command generation
using the local Mistral 7B model via llama.cpp.
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional

# Handle both relative and absolute imports
try:
    from .llama_client import LlamaClient
    from ..tools.registry import ToolRegistry
    from ..common.config import Config
    from ..common.logger import Logger
except ImportError:
    # Add parent directory to path for direct execution
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.agent.llama_client import LlamaClient
    from src.tools.registry import ToolRegistry
    from src.common.config import Config
    from src.common.logger import Logger


class CognosAgent:
    """Main agent class that processes natural language commands."""
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.llama_client = LlamaClient()
        self.tool_registry = ToolRegistry()
        
        # Load system prompt
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load the system prompt for the agent."""
        return """You are CognOS, an AI assistant that helps users interact with their Linux system.

When users ask for file/directory operations, ALWAYS use the appropriate tool instead of just describing what to do.

Common command mappings:
- "show files" / "list files" / "what's here" → use run_command with "ls -la"
- "find directory X" → use search_folder with pattern X
- "go to directory" → use run_command with "cd path"
- "create environment" → use create_env
- "switch environment" → use switch_env

Available tools:
- search_folder: Find directories matching a pattern
- run_command: Execute shell commands safely (USE THIS for ls, cd, cat, etc.)
- list_options: Present multiple choices to the user
- create_env: Create virtual environments
- switch_env: Switch between environments

ALWAYS respond in this JSON format:
{
    "action": "execute",
    "command": "actual shell command",
    "message": "explanation of what will be done",
    "tool_calls": [{"tool": "run_command", "args": {"command": "ls -la"}}]
}

For "show me files" or "list files", ALWAYS use:
{"tool": "run_command", "args": {"command": "ls -la"}}

Be helpful and ALWAYS use tools to perform actual actions, not just descriptions."""
    
    def process_command(self, user_input: str) -> Dict[str, Any]:
        """Process a natural language command and return structured response."""
        try:
            # Prepare the prompt
            prompt = self._build_prompt(user_input)
            
            # Get response from LLM
            response = self.llama_client.generate(prompt)
            
            # Parse JSON response
            try:
                parsed_response = json.loads(response)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                parsed_response = {
                    "action": "info",
                    "message": response,
                    "command": None
                }
            
            # Process any tool calls
            if "tool_calls" in parsed_response:
                parsed_response = self._process_tool_calls(parsed_response)
            
            return parsed_response
            
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            return {
                "action": "info",
                "message": f"Error: {str(e)}",
                "command": None
            }
    
    def _build_prompt(self, user_input: str) -> str:
        """Build the complete prompt for the LLM."""
        # Get current context
        context = self._get_context()
        
        prompt = f"""System: {self.system_prompt}

Context:
- Current directory: {context['pwd']}
- User: {context['user']}
- Operating system: {context['os']}

User request: {user_input}

Response (JSON):"""
        
        return prompt
    
    def _get_context(self) -> Dict[str, Any]:
        """Get current system context."""
        return {
            "pwd": os.getcwd(),
            "user": os.getenv("USER", "unknown"),
            "os": "Linux",
            "hostname": os.getenv("HOSTNAME", "localhost")
        }
    
    def _process_tool_calls(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Process tool calls in the response."""
        if "tool_calls" not in response:
            return response
        
        for tool_call in response["tool_calls"]:
            tool_name = tool_call.get("tool")
            tool_args = tool_call.get("args", {})
            
            if tool_name in self.tool_registry.tools:
                try:
                    tool_result = self.tool_registry.call_tool(tool_name, **tool_args)
                    
                    # Update response with tool result
                    if tool_result.get("command"):
                        response["command"] = tool_result["command"]
                    if tool_result.get("message"):
                        response["message"] = tool_result["message"]
                        
                except Exception as e:
                    self.logger.error(f"Error calling tool {tool_name}: {e}")
                    response["message"] = f"Error using tool {tool_name}: {str(e)}"
        
        return response


def main():
    """Main entry point for standalone agent testing."""
    agent = CognosAgent()
    
    if len(sys.argv) > 1:
        # Process command from command line
        command = " ".join(sys.argv[1:])
        result = agent.process_command(command)
        print(json.dumps(result, indent=2))
    else:
        # Interactive mode
        print("CognOS Agent - Interactive Mode")
        print("Type 'quit' to exit")
        
        while True:
            try:
                user_input = input("Query: ").strip()
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                result = agent.process_command(user_input)
                print(json.dumps(result, indent=2))
                
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
        print("Goodbye!")


if __name__ == "__main__":
    main()