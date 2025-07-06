"""
LLama.cpp client for CognOS AI agent.
"""

import json
import os
from typing import Dict, Any, Optional
from llama_cpp import Llama

# Handle both relative and absolute imports
try:
    from ..common.config import Config
    from ..common.logger import Logger
except ImportError:
    # Add parent directory to path for direct execution
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.common.config import Config
    from src.common.logger import Logger


class LlamaClient:
    """Client interface to llama.cpp for AI inference."""
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the Mistral model via llama.cpp."""
        model_path = self.config.get("agent.model_path", "./models/mistral-7b-q4.gguf")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        try:
            self.model = Llama(
                model_path=model_path,
                n_ctx=self.config.get("agent.context_length", 4096),
                n_threads=4,  # Optimize for Pi
                verbose=False
            )
            self.logger.info(f"Model loaded successfully: {model_path}")
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            raise
    
    def generate(self, prompt: str) -> str:
        """Generate response from the model."""
        if not self.model:
            raise RuntimeError("Model not loaded")
        
        try:
            response = self.model(
                prompt,
                max_tokens=self.config.get("agent.max_tokens", 512),
                temperature=self.config.get("agent.temperature", 0.7),
                stop=["Human:", "User:", "\n\n"]
            )
            
            return response['choices'][0]['text'].strip()
            
        except Exception as e:
            self.logger.error(f"Generation failed: {e}")
            return f"Error: {str(e)}"