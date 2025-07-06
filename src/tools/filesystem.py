"""
Filesystem tools for CognOS agent.
"""

import os
import glob
from typing import Dict, Any, List


class BaseTool:
    """Base class for all CognOS tools."""
    
    def __init__(self):
        self.description = "Base tool"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given arguments."""
        raise NotImplementedError


class SearchFolderTool(BaseTool):
    """Tool for searching directories matching a pattern."""
    
    def __init__(self):
        super().__init__()
        self.description = "Search for directories matching a pattern"
    
    def execute(self, pattern: str = "", path: str = ".", **kwargs) -> Dict[str, Any]:
        """Search for directories matching the pattern."""
        try:
            # Search for directories
            search_pattern = os.path.join(path, f"*{pattern}*")
            matches = []
            
            for item in glob.glob(search_pattern):
                if os.path.isdir(item):
                    matches.append(os.path.abspath(item))
            
            # Also search subdirectories one level deep
            deep_pattern = os.path.join(path, "*", f"*{pattern}*")
            for item in glob.glob(deep_pattern):
                if os.path.isdir(item):
                    matches.append(os.path.abspath(item))
            
            # Remove duplicates and sort
            matches = sorted(list(set(matches)))
            
            if matches:
                return {
                    "action": "info",
                    "message": f"Found {len(matches)} directories matching '{pattern}'",
                    "results": matches[:10],  # Limit to first 10
                    "command": None
                }
            else:
                return {
                    "action": "info",
                    "message": f"No directories found matching '{pattern}'",
                    "results": [],
                    "command": None
                }
                
        except Exception as e:
            return {
                "action": "info",
                "message": f"Error searching directories: {str(e)}",
                "results": [],
                "command": None
            }


class ListOptionsTool(BaseTool):
    """Tool for presenting multiple options to user."""
    
    def __init__(self):
        super().__init__()
        self.description = "Present multiple options for user selection"
    
    def execute(self, options: List[str], message: str = "Please choose:", **kwargs) -> Dict[str, Any]:
        """Present options to user for selection."""
        try:
            if not options:
                return {
                    "action": "info",
                    "message": "No options available",
                    "command": None
                }
            
            # Format options for display
            formatted_options = []
            for i, option in enumerate(options, 1):
                formatted_options.append(f"{i}. {option}")
            
            display_message = f"{message}\n" + "\n".join(formatted_options)
            
            return {
                "action": "question",
                "message": display_message,
                "options": options,
                "command": None
            }
            
        except Exception as e:
            return {
                "action": "info",
                "message": f"Error presenting options: {str(e)}",
                "command": None
            }