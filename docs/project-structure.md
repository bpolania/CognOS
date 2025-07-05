# CognOS Project Structure

## Directory Layout

```
CognOS/
├── src/                    # Source code
│   ├── shell/             # cognos-shell executable
│   │   └── main.py        # Main shell implementation
│   ├── agent/             # AI agent core
│   │   └── main.py        # Agent processing logic
│   ├── tools/             # Agent tools
│   │   └── registry.py    # Tool registry and management
│   ├── ui/                # Desktop overlay (future)
│   └── common/            # Shared utilities
│       ├── config.py      # Configuration management
│       └── logger.py      # Logging utilities
├── config/                # Configuration files
├── scripts/               # Installation and setup scripts
│   ├── install.sh         # Main installation script
│   └── download-models.sh # Model download script
├── models/                # AI models (created during setup)
├── tests/                 # Test files
└── docs/                  # Documentation
```

## Key Components

### Shell (`src/shell/`)
- **main.py**: Main shell executable that replaces user's default shell
- Handles command interception and routing
- Manages session state and user interaction

### Agent (`src/agent/`)
- **main.py**: Core AI processing using Mistral 7B
- Handles natural language understanding
- Manages tool calling and response generation

### Tools (`src/tools/`)
- **registry.py**: Central registry for all agent tools
- Individual tool implementations for system operations

### Common (`src/common/`)
- **config.py**: Configuration management with JSON files
- **logger.py**: Structured logging with file rotation

## Development Workflow

1. **Setup**: Run `make setup` to create virtual environment and install dependencies
2. **Models**: Run `make models` to download required AI models
3. **Build**: Run `make build` to compile components
4. **Install**: Run `make install` to install system-wide
5. **Test**: Run `make test` to run test suite

## Configuration

- **System Config**: `/etc/cognos/config.json`
- **User Config**: `~/.config/cognos/config.json`
- **Logs**: `~/.local/share/cognos/cognos.log`

## Next Steps

1. Implement llama.cpp integration in agent
2. Build basic filesystem tools
3. Add shell command classification
4. Implement safety confirmation system
5. Add comprehensive testing