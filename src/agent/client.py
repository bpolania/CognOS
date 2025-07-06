"""
Agent client for shell integration.
"""

import json
import os
import sys
from typing import Dict, Any

# Handle both relative and absolute imports
try:
    from .main import CognosAgent
except ImportError:
    # Add parent directory to path for direct execution
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.agent.main import CognosAgent


class AgentClient:
    """Client interface for shell to communicate with CognOS agent."""
    
    def __init__(self):
        self.agent = CognosAgent()
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """Process a command through the agent and return structured response."""
        return self.agent.process_command(command)