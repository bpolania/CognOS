# CognOS Makefile

.PHONY: help setup build install test clean models

# Default target
help:
	@echo "CognOS Development Commands:"
	@echo "  setup    - Initial setup (install dependencies)"
	@echo "  build    - Build all components"
	@echo "  install  - Install CognOS as default shell"
	@echo "  test     - Run tests"
	@echo "  clean    - Clean build artifacts"
	@echo "  models   - Download required models"

# Setup development environment
setup:
	sudo apt-get update
	sudo apt-get install -y python3-pip python3-venv build-essential cmake
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	@echo "Setup complete. Activate with: source venv/bin/activate"

# Build all components
build:
	@echo "Building cognos-shell..."
	$(MAKE) -C src/shell
	@echo "Building cognos-ui..."
	$(MAKE) -C src/ui
	@echo "Build complete"

# Install CognOS as default shell
install: build
	@echo "Installing CognOS..."
	sudo cp src/shell/cognos-shell /usr/local/bin/
	sudo chmod +x /usr/local/bin/cognos-shell
	@echo "Adding to /etc/shells..."
	grep -q "/usr/local/bin/cognos-shell" /etc/shells || echo "/usr/local/bin/cognos-shell" | sudo tee -a /etc/shells
	@echo "Installation complete. Change default shell with: chsh -s /usr/local/bin/cognos-shell"

# Run tests
test:
	./venv/bin/pytest tests/ -v

# Clean build artifacts
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info/
	$(MAKE) -C src/shell clean
	$(MAKE) -C src/ui clean

# Download models
models:
	scripts/download-models.sh