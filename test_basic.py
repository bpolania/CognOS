#!/usr/bin/env python3
"""
Basic test script to verify CognOS components work.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all components can be imported."""
    print("Testing imports...")
    
    try:
        from src.common.config import Config
        print("✓ Config import successful")
    except Exception as e:
        print(f"✗ Config import failed: {e}")
        return False
    
    try:
        from src.common.logger import Logger
        print("✓ Logger import successful")
    except Exception as e:
        print(f"✗ Logger import failed: {e}")
        return False
    
    try:
        from src.tools.registry import ToolRegistry
        print("✓ ToolRegistry import successful")
    except Exception as e:
        print(f"✗ ToolRegistry import failed: {e}")
        return False
    
    try:
        from src.tools.filesystem import SearchFolderTool
        print("✓ SearchFolderTool import successful")
    except Exception as e:
        print(f"✗ SearchFolderTool import failed: {e}")
        return False
    
    return True

def test_tools():
    """Test basic tool functionality."""
    print("\nTesting tools...")
    
    try:
        from src.tools.registry import ToolRegistry
        registry = ToolRegistry()
        
        # Test search_folder tool
        result = registry.call_tool("search_folder", pattern="test", path=".")
        print(f"✓ search_folder tool works: {result['action']}")
        
        # Test list tools
        tools = registry.list_tools()
        print(f"✓ Available tools: {list(tools.keys())}")
        
        return True
    except Exception as e:
        print(f"✗ Tool testing failed: {e}")
        return False

def test_llama_import():
    """Test llama-cpp-python import."""
    print("\nTesting llama-cpp-python...")
    
    try:
        from llama_cpp import Llama
        print("✓ llama-cpp-python import successful")
        return True
    except Exception as e:
        print(f"✗ llama-cpp-python import failed: {e}")
        print("  This is expected if the model isn't downloaded yet")
        return False

def main():
    """Run all tests."""
    print("CognOS Basic Component Test")
    print("=" * 40)
    
    success = True
    
    success &= test_imports()
    success &= test_tools()
    success &= test_llama_import()
    
    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed - check output above")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())