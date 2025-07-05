"""
Configuration management for CognOS.
"""

import json
import os
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for CognOS."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()
    
    def _get_default_config_path(self) -> str:
        """Get the default configuration file path."""
        # Try user config directory first
        config_dir = os.path.expanduser("~/.config/cognos")
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
        
        return os.path.join(config_dir, "config.json")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        default_config = {
            "agent": {
                "model_path": "/opt/cognos/models/mistral-7b-q4.gguf",
                "context_length": 4096,
                "temperature": 0.7,
                "max_tokens": 512
            },
            "shell": {
                "confirmation_required": True,
                "log_commands": True,
                "safe_mode": True
            },
            "ui": {
                "theme": "dark",
                "hotkey": "ctrl+space",
                "window_size": [600, 400]
            },
            "tools": {
                "search_folder": {"enabled": True, "max_results": 10},
                "run_command": {"enabled": True, "timeout": 30},
                "create_env": {"enabled": True, "default_python": "python3"}
            },
            "logging": {
                "level": "INFO",
                "file": "~/.local/share/cognos/cognos.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    return self._merge_config(default_config, user_config)
            except Exception as e:
                print(f"Error loading config: {e}")
                return default_config
        else:
            # Create default config file
            self._save_config(default_config)
            return default_config
    
    def _merge_config(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Merge user configuration with defaults."""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get a configuration value using dot notation."""
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """Set a configuration value using dot notation."""
        keys = key_path.split('.')
        config = self.config
        
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        config[keys[-1]] = value
        self._save_config(self.config)
    
    def reload(self):
        """Reload configuration from file."""
        self.config = self._load_config()