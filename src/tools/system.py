"""
System tools for CognOS agent.
"""

import subprocess
import shlex
from typing import Dict, Any

from .filesystem import BaseTool


class RunCommandTool(BaseTool):
    """Tool for safely executing shell commands."""
    
    def __init__(self):
        super().__init__()
        self.description = "Execute shell commands safely with user confirmation"
    
    def execute(self, command: str, **kwargs) -> Dict[str, Any]:
        """Execute a shell command safely."""
        try:
            # Basic safety checks
            dangerous_commands = [
                'rm -rf /', 'rm -rf /*', 'mkfs', 'dd if=', 'format',
                'del /f /s /q', 'shutdown', 'reboot', 'halt',
                'passwd', 'userdel', 'usermod'
            ]
            
            command_lower = command.lower().strip()
            for dangerous in dangerous_commands:
                if dangerous in command_lower:
                    return {
                        "action": "info",
                        "message": f"Command '{command}' is potentially dangerous and blocked for safety",
                        "command": None
                    }
            
            # Return command for user confirmation
            return {
                "action": "execute",
                "message": f"Ready to execute: {command}",
                "command": command
            }
            
        except Exception as e:
            return {
                "action": "info",
                "message": f"Error preparing command: {str(e)}",
                "command": None
            }
    
    def _execute_command(self, command: str) -> str:
        """Actually execute the command (called after user confirmation)."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return f"Error: {result.stderr.strip()}"
                
        except subprocess.TimeoutExpired:
            return "Error: Command timed out"
        except Exception as e:
            return f"Error: {str(e)}"