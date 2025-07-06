# CognOS: AI-Augmented Operating System

CognOS is an AI-augmented operating system that provides natural language command interpretation through local language models. The system translates user intent into real system commands, automates environment setup, and provides an interactive, context-aware interface that makes managing Linux environments more accessible and intuitive.

## Project Overview

CognOS offers two deployment models:

- **[CognOS Prototype](COGNOS_PROTOTYPE.md)**: Pre-configured Raspberry Pi OS image for demos and testing
- **[CognOS Distribution](COGNOS_DISTRIBUTION.md)**: Complete custom Linux distribution for production deployment

## Core Technology

- **AI Engine**: Mistral 7B (Q4/Q5 quantized) via llama.cpp
- **Architecture**: Custom shell replacement with AI agent integration
- **Tools**: Extensible tool system for filesystem, environment, and application management
- **Safety**: User confirmation and comprehensive logging for all AI actions

---

## Repository Structure

```
CognOS/
├── src/                    # Source code
│   ├── shell/             # cognos-shell executable
│   ├── agent/             # AI agent core
│   ├── tools/             # Agent tools (search_folder, run_command, etc.)
│   ├── ui/                # Desktop overlay (future)
│   └── common/            # Shared utilities (config, logging)
├── config/                # Configuration templates
├── scripts/               # Installation and setup scripts
├── models/                # AI models (downloaded during setup)
├── tests/                 # Test suite
└── docs/                  # Documentation
```

## Core Architecture

### Shell Layer
- **Custom Shell**: `cognos-shell` executable replaces user's default shell
- **Command Interception**: Distinguishes natural language from direct shell commands
- **AI Integration**: Routes natural language to Mistral 7B agent
- **Safety Layer**: User confirmation for all AI-generated commands

### AI Agent
- **Local LLM**: Mistral 7B Q4/Q5 via llama.cpp
- **Tool System**: Extensible tool registry with safety controls
- **Function Calling**: Structured JSON responses with tool execution
- **Logging**: Comprehensive audit trail of all AI decisions

### Tool Ecosystem
- **search_folder**: Filesystem navigation and discovery
- **list_options**: Multi-choice selection interface
- **run_command**: Safe shell command execution
- **create_env/switch_env**: Python environment management
- **Extensible**: Plugin architecture for custom tools

### User Interface
- **Primary**: Enhanced shell with natural language processing
- **Optional**: Desktop overlay with global hotkey activation
- **Integration**: ChatGPT API for general-purpose queries

---

## Quick Start

### Development Setup
```bash
# Clone repository
git clone https://github.com/bpolania/CognOS.git
cd CognOS

# Setup environment (requires Python 3.8+)
make setup

# Download AI models
make models

# Build and test
make build
make test
```

### Installation
```bash
# Install system-wide
make install

# Set as default shell
chsh -s /usr/local/bin/cognos-shell
```

## Development

- **[Development Setup](docs/development-setup.md)**: Complete setup guide for Mac + Raspberry Pi development
- **[Project Structure](docs/project-structure.md)**: Detailed codebase organization
- **[Changelog](CHANGELOG.md)**: Development history and session logs

## Configuration

- **System**: `/etc/cognos/config.json`
- **User**: `~/.config/cognos/config.json`
- **Logs**: `~/.local/share/cognos/cognos.log`
- **Models**: `./models/mistral-7b-q4.gguf`

## Contributing

1. Read the appropriate deployment documentation ([Prototype](COGNOS_PROTOTYPE.md) or [Distribution](COGNOS_DISTRIBUTION.md))
2. Set up development environment using [Development Setup](docs/development-setup.md)
3. Follow the development phases and contribute to the current phase
4. Update changelog for code changes (documentation-only changes excluded)

---

*CognOS: Making Linux environments more accessible through natural language AI interaction*