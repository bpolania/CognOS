"""
Agent client for shell integration.
"""

import json
from typing import Dict, Any

from .main import CognosAgent


class AgentClient:
    """Client interface for shell to communicate with CognOS agent."""
    
    def __init__(self):
        self.agent = CognosAgent()
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """Process a command through the agent and return structured response."""
        return self.agent.process_command(command)