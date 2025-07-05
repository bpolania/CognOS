"""
Logging utilities for CognOS.
"""

import logging
import os
from typing import Optional
from logging.handlers import RotatingFileHandler


class Logger:
    """Logger utility for CognOS."""
    
    def __init__(self, name: str = "cognos", config=None):
        self.name = name
        self.config = config
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up the logger with appropriate handlers."""
        logger = logging.getLogger(self.name)
        
        # Prevent duplicate handlers
        if logger.handlers:
            return logger
        
        # Get configuration
        if self.config:
            log_level = self.config.get("logging.level", "INFO")
            log_file = self.config.get("logging.file", "~/.local/share/cognos/cognos.log")
            max_size = self.config.get("logging.max_size", "10MB")
            backup_count = self.config.get("logging.backup_count", 5)
        else:
            log_level = "INFO"
            log_file = "~/.local/share/cognos/cognos.log"
            max_size = "10MB"
            backup_count = 5
        
        # Set log level
        logger.setLevel(getattr(logging, log_level.upper()))
        
        # Create log directory if it doesn't exist
        log_file = os.path.expanduser(log_file)
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)  # Only warnings and errors to console
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler with rotation
        max_bytes = self._parse_size(max_size)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def _parse_size(self, size_str: str) -> int:
        """Parse size string like '10MB' to bytes."""
        size_str = size_str.upper()
        
        if size_str.endswith('KB'):
            return int(size_str[:-2]) * 1024
        elif size_str.endswith('MB'):
            return int(size_str[:-2]) * 1024 * 1024
        elif size_str.endswith('GB'):
            return int(size_str[:-2]) * 1024 * 1024 * 1024
        else:
            return int(size_str)
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.logger.debug(message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self.logger.info(message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.logger.warning(message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self.logger.error(message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.logger.critical(message, **kwargs)
    
    def command(self, command: str, user: str = None, result: str = None):
        """Log command execution."""
        user = user or os.getenv("USER", "unknown")
        log_msg = f"Command executed by {user}: {command}"
        if result:
            log_msg += f" | Result: {result}"
        self.logger.info(log_msg)