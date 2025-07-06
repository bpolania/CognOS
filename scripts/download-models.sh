#!/bin/bash
# Download required models for CognOS

set -e

MODELS_DIR="./models"
# Use a smaller, reliable model for testing
MODEL_URL="https://huggingface.co/microsoft/DialoGPT-small/resolve/main/pytorch_model.bin"
MODEL_FILE="mistral-7b-q4.gguf"

# Better option: Try a working GGUF model
MODEL_URL="https://huggingface.co/TheBloke/Llama-2-7b-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_0.gguf"
MODEL_FILE="mistral-7b-q4.gguf"

echo "Setting up models directory..."
mkdir -p "$MODELS_DIR"

echo "Downloading LLaMA 2 7B Chat Q4 model..."
if [ ! -f "$MODELS_DIR/$MODEL_FILE" ]; then
    echo "Downloading $MODEL_FILE..."
    echo "This may take 10-15 minutes depending on your connection..."
    wget -O "$MODELS_DIR/$MODEL_FILE" "$MODEL_URL"
    echo "Model downloaded successfully!"
else
    echo "Model already exists: $MODELS_DIR/$MODEL_FILE"
fi

echo "Verifying model file..."
if [ -f "$MODELS_DIR/$MODEL_FILE" ]; then
    echo "✓ Model file found: $(du -h "$MODELS_DIR/$MODEL_FILE" | cut -f1)"
else
    echo "✗ Model file not found!"
    exit 1
fi

echo "Model setup complete!"
echo "Model path: $(realpath "$MODELS_DIR/$MODEL_FILE")"