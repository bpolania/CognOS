#!/usr/bin/env python3
"""
CognOS Shell - AI-Enhanced Command Line Interface

This is the main entry point for the cognos-shell executable.
It replaces the user's default shell and provides natural language
command interpretation through the AI agent.
"""

import sys
import os
import subprocess
import signal
from typing import Optional

# Handle both relative and absolute imports
try:
    from ..agent.client import AgentClient
    from ..common.config import Config
    from ..common.logger import Logger
except ImportError:
    # Add parent directory to path for direct execution
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.agent.client import AgentClient
    from src.common.config import Config
    from src.common.logger import Logger


class CognosShell:
    """Main shell class that handles command interpretation and execution."""
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.agent = AgentClient()
        self.running = True
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_terminate)
    
    def _handle_interrupt(self, signum, frame):
        """Handle Ctrl+C interrupt."""
        print("\nUse 'exit' to quit cognos-shell")
    
    def _handle_terminate(self, signum, frame):
        """Handle termination signal."""
        self.running = False
    
    def is_natural_language(self, command: str) -> bool:
        """Determine if command is natural language or direct shell command."""
        # Simple heuristics - can be enhanced with ML
        natural_indicators = [
            "please", "can you", "help me", "show me", "find", "search",
            "go to", "navigate", "open", "create", "make", "install"
        ]
        
        # Check for common shell commands
        shell_commands = [
            "ls", "cd", "pwd", "cat", "grep", "find", "chmod", "chown",
            "git", "python", "pip", "sudo", "apt", "systemctl"
        ]
        
        first_word = command.strip().split()[0].lower()
        
        # If starts with shell command, likely direct
        if first_word in shell_commands:
            return False
        
        # If contains natural language indicators, likely natural
        if any(indicator in command.lower() for indicator in natural_indicators):
            return True
        
        # Default to natural language for complex sentences
        return len(command.split()) > 3
    
    def execute_shell_command(self, command: str) -> int:
        """Execute a direct shell command."""
        try:
            result = subprocess.run(command, shell=True, capture_output=False)
            return result.returncode
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return 1
    
    def process_natural_language(self, command: str) -> int:
        """Process natural language command through AI agent."""
        try:
            response = self.agent.process_command(command)
            
            if response.get("action") == "execute":
                shell_command = response.get("command")
                if shell_command:
                    print(f"Executing: {shell_command}")
                    if input("Continue? (y/n): ").lower() == 'y':
                        return self.execute_shell_command(shell_command)
                    else:
                        print("Command cancelled.")
                        return 0
            else:
                print(response.get("message", "Command processed."))
                return 0
                
        except Exception as e:
            self.logger.error(f"Error processing natural language: {e}")
            print(f"Error: {e}")
            return 1
    
    def run(self):
        """Main shell loop."""
        print("CognOS Shell - AI-Enhanced Command Line")
        print("Type 'help' for assistance or 'exit' to quit")
        
        while self.running:
            try:
                # Get current directory for prompt
                cwd = os.getcwd()
                username = os.getenv("USER", "user")
                hostname = os.getenv("HOSTNAME", "cognos")
                
                # Display prompt
                prompt = f"{username}@{hostname}:{cwd}$ "
                command = input(prompt).strip()
                
                if not command:
                    continue
                
                # Handle built-in commands
                if command.lower() in ['exit', 'quit']:
                    break
                elif command.lower() == 'help':
                    self.show_help()
                    continue
                
                # Determine if natural language or direct command
                if self.is_natural_language(command):
                    self.process_natural_language(command)
                else:
                    self.execute_shell_command(command)
                    
            except EOFError:
                # Handle Ctrl+D
                break
            except KeyboardInterrupt:
                # Handle Ctrl+C
                print()
                continue
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                print(f"Error: {e}")
        
        print("Goodbye!")
    
    def show_help(self):
        """Show help information."""
        print("""
CognOS Shell Help:
- Use natural language: "go to my documents folder"
- Use direct commands: "ls -la"
- Type 'exit' to quit
- Type 'help' for this message

Natural language examples:
- "show me files in the current directory"
- "find all python files in this project"
- "go to the downloads folder"
- "install python package requests"
""")


def main():
    """Main entry point for cognos-shell."""
    shell = CognosShell()
    shell.run()


if __name__ == "__main__":
    main()