"""
Environment management tools for CognOS agent.
"""

import os
import subprocess
from typing import Dict, Any

from .filesystem import BaseTool


class CreateEnvTool(BaseTool):
    """Tool for creating Python virtual environments."""
    
    def __init__(self):
        super().__init__()
        self.description = "Create Python virtual environments"
    
    def execute(self, name: str, python_version: str = "python3", **kwargs) -> Dict[str, Any]:
        """Create a new virtual environment."""
        try:
            if not name:
                return {
                    "action": "info",
                    "message": "Environment name is required",
                    "command": None
                }
            
            # Create command to make virtual environment
            env_path = os.path.expanduser(f"~/venvs/{name}")
            command = f"{python_version} -m venv {env_path}"
            
            return {
                "action": "execute",
                "message": f"Ready to create virtual environment '{name}' at {env_path}",
                "command": command
            }
            
        except Exception as e:
            return {
                "action": "info",
                "message": f"Error preparing environment creation: {str(e)}",
                "command": None
            }


class SwitchEnvTool(BaseTool):
    """Tool for switching between virtual environments."""
    
    def __init__(self):
        super().__init__()
        self.description = "Switch between Python virtual environments"
    
    def execute(self, name: str, **kwargs) -> Dict[str, Any]:
        """Switch to a virtual environment."""
        try:
            if not name:
                return {
                    "action": "info",
                    "message": "Environment name is required",
                    "command": None
                }
            
            env_path = os.path.expanduser(f"~/venvs/{name}")
            activate_script = os.path.join(env_path, "bin", "activate")
            
            if not os.path.exists(activate_script):
                return {
                    "action": "info",
                    "message": f"Virtual environment '{name}' not found at {env_path}",
                    "command": None
                }
            
            command = f"source {activate_script}"
            
            return {
                "action": "execute",
                "message": f"Ready to activate virtual environment '{name}'",
                "command": command
            }
            
        except Exception as e:
            return {
                "action": "info",
                "message": f"Error preparing environment switch: {str(e)}",
                "command": None
            }