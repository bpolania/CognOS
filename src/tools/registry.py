"""
Tool Registry - Manages available tools for the AI agent.
"""

from typing import Dict, Any, Callable
from .filesystem import SearchFolderTool, ListOptionsTool
from .system import RunCommandTool
from .environment import CreateEnvTool, SwitchEnvTool


class ToolRegistry:
    """Registry for all available agent tools."""
    
    def __init__(self):
        self.tools: Dict[str, Callable] = {}
        self._register_tools()
    
    def _register_tools(self):
        """Register all available tools."""
        # Filesystem tools
        self.tools["search_folder"] = SearchFolderTool()
        self.tools["list_options"] = ListOptionsTool()
        
        # System tools
        self.tools["run_command"] = RunCommandTool()
        
        # Environment tools
        self.tools["create_env"] = CreateEnvTool()
        self.tools["switch_env"] = SwitchEnvTool()
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a tool with the given arguments."""
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        tool = self.tools[tool_name]
        return tool.execute(**kwargs)
    
    def list_tools(self) -> Dict[str, str]:
        """List all available tools and their descriptions."""
        return {
            name: tool.description 
            for name, tool in self.tools.items()
        }