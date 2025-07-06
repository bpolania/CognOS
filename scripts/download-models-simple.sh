#!/bin/bash
# Simple model download for CognOS testing

set -e

MODELS_DIR="./models"
echo "Setting up models directory..."
mkdir -p "$MODELS_DIR"

echo "For now, we'll test without the model. To add a model later:"
echo "1. Download any GGUF model manually to ./models/"
echo "2. Update the model path in ~/.config/cognos/config.json"
echo ""
echo "Popular model sources:"
echo "- https://huggingface.co/models?library=gguf"
echo "- Search for 'mistral GGUF' or 'llama GGUF'"
echo ""
echo "For testing, we can run the agent without a model first."

# Create a placeholder
touch "$MODELS_DIR/README.txt"
echo "Place GGUF model files here" > "$MODELS_DIR/README.txt"

echo "Model directory setup complete!"
echo "You can test the agent components without a model first."