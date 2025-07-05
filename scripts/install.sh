#!/bin/bash
"""
Installation script for CognOS.
"""

set -e

echo "Installing CognOS..."

# Check if running on supported system
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Error: CognOS is designed for Linux systems"
    exit 1
fi

# Check for required dependencies
echo "Checking dependencies..."
command -v python3 >/dev/null 2>&1 || { echo "Error: python3 is required but not installed."; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "Error: pip3 is required but not installed."; exit 1; }

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download models
echo "Downloading models..."
./scripts/download-models.sh

# Build components
echo "Building components..."
make build

# Install CognOS
echo "Installing CognOS system-wide..."
sudo make install

echo ""
echo "Installation complete!"
echo ""
echo "To set CognOS as your default shell:"
echo "  chsh -s /usr/local/bin/cognos-shell"
echo ""
echo "To test CognOS without changing your default shell:"
echo "  /usr/local/bin/cognos-shell"
echo ""
echo "Configuration: ~/.config/cognos/config.json"
echo "Logs: ~/.local/share/cognos/cognos.log"