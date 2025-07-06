#!/bin/bash
# Download required models for CognOS

set -e

MODELS_DIR="./models"
# Use TinyLlama 1.1B model optimized for Raspberry Pi
MODEL_URL="https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
MODEL_FILE="mistral-7b-q4.gguf"

echo "Setting up models directory..."
mkdir -p "$MODELS_DIR"

echo "Downloading TinyLlama 1.1B Chat Q4 model (optimized for Raspberry Pi)..."
if [ ! -f "$MODELS_DIR/$MODEL_FILE" ]; then
    echo "Downloading $MODEL_FILE..."
    echo "File size: ~1.1GB - This should take 3-5 minutes depending on your connection..."
    wget -O "$MODELS_DIR/$MODEL_FILE" "$MODEL_URL"
    echo "TinyLlama model downloaded successfully!"
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