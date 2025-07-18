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
    
    def is_safe_command(self, command: str) -> bool:
        """Check if a command is safe to execute without confirmation."""
        safe_commands = [
            "ls", "ll", "la", "pwd", "whoami", "date", "uptime",
            "df", "free", "cat", "head", "tail", "less", "more",
            "grep", "find", "which", "echo", "printenv", "history"
        ]
        
        # Get the first word (the actual command)
        first_word = command.strip().split()[0].lower()
        
        # Check if it's a safe read-only command
        if first_word in safe_commands:
            return True
        
        # Special cases for ls variants
        if first_word.startswith("ls"):
            return True
            
        return False
    
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
    
    def get_confirmation_message(self, command: str) -> str:
        """Generate a context-aware confirmation message using the AI agent."""
        # For smaller models like TinyLlama, use fallback explanations directly
        # to avoid confusing or incorrect LLM responses
        explanation = self._get_fallback_explanation(command)
        return f"{explanation}\nContinue? (y/n): "
    
    def _get_fallback_explanation(self, command: str) -> str:
        """Provide fallback explanations for common commands."""
        parts = command.strip().split()
        if not parts:
            return f"This will execute: {command}"
            
        first_word = parts[0].lower()
        
        # Extract actual filename/path from command, skipping flags
        def get_target_file(parts, start_idx=1):
            """Extract the actual filename from command parts, skipping flags."""
            for i in range(start_idx, len(parts)):
                if not parts[i].startswith('-'):
                    return parts[i]
            return None
        
        if first_word == "touch":
            target = get_target_file(parts)
            if target:
                return f"This will create an empty file named '{target}'."
            else:
                return "This will create an empty file or update its timestamp."
        elif first_word == "mkdir":
            target = get_target_file(parts)
            if target:
                return f"This will create a new directory named '{target}'."
            else:
                return "This will create a new directory."
        elif first_word == "rm":
            target = get_target_file(parts)
            if target:
                if "-rf" in command or "-r" in command:
                    return f"This will permanently delete '{target}' and all its contents."
                else:
                    return f"This will delete the file '{target}'."
            else:
                return "This will delete files or directories."
        elif first_word == "cp":
            # For cp, we need source and destination
            source = get_target_file(parts)
            if source and len(parts) >= 3:
                # Find destination (last non-flag argument)
                dest = None
                for i in range(len(parts) - 1, 0, -1):
                    if not parts[i].startswith('-'):
                        dest = parts[i]
                        break
                if dest and dest != source:
                    return f"This will copy '{source}' to '{dest}'."
            return "This will copy files or directories."
        elif first_word == "mv":
            # For mv, we need source and destination
            source = get_target_file(parts)
            if source and len(parts) >= 3:
                # Find destination (last non-flag argument)
                dest = None
                for i in range(len(parts) - 1, 0, -1):
                    if not parts[i].startswith('-'):
                        dest = parts[i]
                        break
                if dest and dest != source:
                    return f"This will move '{source}' to '{dest}'."
            return "This will move or rename files or directories."
        elif first_word == "cat":
            target = get_target_file(parts)
            if target:
                return f"This will display the contents of '{target}'."
            else:
                return "This will display the contents of a file."
        elif first_word == "echo":
            return "This will output text to the terminal."
        elif first_word == "cd":
            target = get_target_file(parts)
            if target:
                return f"This will change to the directory '{target}'."
            else:
                return "This will change the current directory."
        elif first_word == "ls":
            return "This will list files and directories."
        elif first_word == "pwd":
            return "This will show the current directory path."
        else:
            # Generic fallbacks for common commands
            fallback_explanations = {
                "touch": "This will create an empty file or update its timestamp.",
                "mkdir": "This will create a new directory.",
                "rm": "This will delete files or directories.",
                "cp": "This will copy files or directories.",
                "mv": "This will move or rename files or directories.",
                "ls": "This will list files and directories.",
                "cat": "This will display the contents of a file.",
                "echo": "This will output text to the terminal.",
                "cd": "This will change the current directory.",
                "pwd": "This will show the current directory path."
            }
            
            return fallback_explanations.get(first_word, f"This will execute: {command}")
    
    def process_natural_language(self, command: str) -> int:
        """Process natural language command through AI agent."""
        try:
            response = self.agent.process_command(command)
            
            if response.get("action") == "execute":
                shell_command = response.get("command")
                if shell_command:
                    # Check if it's a safe command that doesn't need confirmation
                    if self.is_safe_command(shell_command):
                        print(f"→ {shell_command}")
                        return self.execute_shell_command(shell_command)
                    else:
                        # Use context-aware confirmation message
                        confirmation_msg = self.get_confirmation_message(shell_command)
                        user_input = input(confirmation_msg).lower()
                        
                        # Handle different confirmation responses
                        if user_input in ['y', 'yes']:
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