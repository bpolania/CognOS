#!/bin/bash
# Download required models for CognOS

set -e

MODELS_DIR="./models"
MISTRAL_URL="https://huggingface.co/microsoft/DialoGPT-medium/resolve/main/pytorch_model.bin"
MISTRAL_FILE="mistral-7b-q4.gguf"

# Alternative: Use a working GGUF model URL
MISTRAL_URL="https://huggingface.co/bartowski/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/Mistral-7B-Instruct-v0.3-Q4_K_M.gguf"

echo "Setting up models directory..."
mkdir -p "$MODELS_DIR"

echo "Downloading Mistral 7B Q4 model..."
if [ ! -f "$MODELS_DIR/$MISTRAL_FILE" ]; then
    echo "Downloading $MISTRAL_FILE..."
    wget -O "$MODELS_DIR/$MISTRAL_FILE" "$MISTRAL_URL"
    echo "Model downloaded successfully!"
else
    echo "Model already exists: $MODELS_DIR/$MISTRAL_FILE"
fi

echo "Verifying model file..."
if [ -f "$MODELS_DIR/$MISTRAL_FILE" ]; then
    echo "✓ Model file found: $(du -h "$MODELS_DIR/$MISTRAL_FILE" | cut -f1)"
else
    echo "✗ Model file not found!"
    exit 1
fi

echo "Model setup complete!"
echo "Model path: $(realpath "$MODELS_DIR/$MISTRAL_FILE")"