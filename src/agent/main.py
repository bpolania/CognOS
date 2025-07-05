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

from .llama_client import LlamaClient
from ..tools.registry import ToolRegistry
from ..common.config import Config
from ..common.logger import Logger


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
        
Your role is to:
1. Understand natural language commands from users
2. Translate them into appropriate system commands or tool calls
3. Provide helpful explanations and confirmations

Available tools:
- search_folder: Find directories matching a pattern
- run_command: Execute shell commands safely
- list_options: Present multiple choices to the user
- create_env: Create virtual environments
- switch_env: Switch between environments

Always respond in JSON format with:
{
    "action": "execute|info|question",
    "command": "shell command to run (if action=execute)",
    "message": "explanation or response",
    "tool_calls": [{"tool": "tool_name", "args": {...}}]
}

Be helpful but always prioritize safety. Ask for confirmation before destructive operations."""
    
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