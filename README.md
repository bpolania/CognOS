# CognOS: General Development Plan

CognOS is an AI-augmented operating system layer designed for Raspberry Pi. It combines a local language model acting as an intelligent command-line agent with a desktop overlay for natural-language control. The system translates user intent into real system commands, automates environment setup, and provides an interactive, context-aware interface that makes managing a Linux environment more accessible and intuitive.

**Base OS:**  
Raspberry Pi OS (64-bit)

---

**LLM Choice:**  
- Use **Mistral 7B**, quantized to **Q4** or **Q5**, running with **llama.cpp**.
- This model supports instruct-style responses and can run locally on an 8 GB Raspberry Pi (with swap if needed).
- Suitable for reasoning and agent-like planning needed for CLI-level automation.

---

## SHELL (CLI-LEVEL)

*Goal:* Build an AI-enhanced shell that uses Mistral 7B in agent mode to interpret natural language, plan multi-step interactions, and execute system commands safely.

---

### Shell Wrapper Architecture
CognOS implements a **custom shell replacement** approach that becomes the user's default shell on system startup.

**Core Architecture:**
- Create `cognos-shell` executable that wraps bash/zsh functionality
- Intercept all command input and determine if it's natural language or direct shell commands
- Route natural language commands to AI agent, pass through direct commands to underlying shell
- Maintain shell session state (pwd, env vars, history) across AI interactions
- Support both interactive and non-interactive modes

**Implementation Steps:**
1. **Build `cognos-shell`** - create executable that handles both AI and standard shell commands
2. **Register shell** - add to `/etc/shells` as valid shell option
3. **Set as default** - update user's shell in `/etc/passwd` or via `chsh` command
4. **Fallback support** - users can still access bash directly if needed (`/bin/bash`)

---

### NLP Agent Layer
- Install and configure **llama.cpp** on Raspberry Pi OS.
- Load **Mistral 7B Q4/Q5 quantized model**.
- Define prompt templates for agent-style function calling (e.g., `search_folder`, `run_command`, `list_options`).
- Build a function-calling interface that exposes controlled tools the agent can use.
- Log all agent decisions and tool calls for user review.
- **Agent Communication Protocol** - define standard interface between shell wrapper and AI agent

---

### Agent Tools
- **search_folder**: searches filesystem for matching directory names.
- **list_options**: presents multiple search results for user selection.
- **run_command**: safely executes shell commands with confirmation.
- **create_env** and **switch_env**: manage scoped virtual environments.
- Define clear, well-documented interfaces for all tools to ensure safety and predictability.

---

### Enhanced “go to” Command (Agent Behavior)
- User issues request like: “go to the photos folder from last year.”
- Agent calls **search_folder** with the parsed target.
- System returns matching paths.
- Agent calls **list_options** to present choices.
- User selects an option.
- Agent calls **run_command** to perform `cd` into the selected path.
- Agent maintains context to handle follow-up refinements.

---

### Automated Environment Setup (Agent Behavior, Scoped)
- Define JSON/YAML recipes with known, working package lists for Raspberry Pi.
- Agent maps user instructions to available recipes via prompt parsing.
- Agent calls **create_env** to create venv and install specified packages.
- Support **list_envs** and **switch_env** tools for managing environments.
- Agent confirms planned actions before execution and handles errors with fallback instructions.

---

### Safety and Transparency
- All agent tool calls logged with parameters and results.
- Require explicit user confirmation for elevated or destructive commands.
- Provide option to display exact shell command before execution.
- Allow user to enable/disable individual tools for additional control.

---

## UI-LEVEL

*Goal:* Build a desktop overlay prompt that acts as an AI command launcher, using the same agent layer locally for command automation and ChatGPT API for general-purpose prompts.

---

### Overlay Prompt Window
- Develop a GTK/QT app with text input and result display.
- Set up global shortcut (like Command+Spacebar) to open overlay from desktop.
- Include simple, clear styling for usability.

---

### Agent Integration in UI
- Route command-related prompts to local **Mistral 7B** agent.
- Display agent responses and tool call results in real time.
- Show previews and request user confirmation for all planned actions.
- Maintain conversation context for multi-step or clarifying interactions.

---

### General-Purpose Prompts via ChatGPT API
- Route non-automation prompts (summaries, writing help, creative tasks) to ChatGPT API.
- Distinguish between local agent commands and cloud-based general tasks.
- Clearly indicate which prompts are local vs. remote for user transparency.

---

### App and File Launcher (Agent Behavior)
- Agent interprets commands like “open LibreOffice” or “show my PDF files.”
- Calls **search_app** and **launch_app** tools to find and open installed apps.
- Supports opening files with default or user-specified apps.

---

### Context Awareness (Optional / Later)
- Store recent commands, paths, and environment setups in local history.
- Allow agent to suggest next actions or auto-complete commands based on history.
- Include management tools for clearing or reviewing history.

---

## DEVELOPMENT PHASES

### Phase 1: Foundation (Custom Shell + Basic Agent)
1. **llama.cpp Setup** - install and configure on Pi, test Mistral 7B inference
2. **cognos-shell Prototype** - create basic custom shell executable with command interception
3. **Agent Core** - build minimal Python wrapper around llama.cpp with function calling
4. **Tool Integration** - implement `search_folder` and `run_command` tools
5. **Shell Registration** - add to `/etc/shells` and set as user's default shell
6. **Basic Testing** - verify natural language → shell command flow from system startup

### Phase 2: Shell Enhancement
1. **Session Management** - maintain shell state across AI interactions
2. **Command Classification** - distinguish natural language vs direct commands
3. **Safety Layer** - implement confirmation prompts and command logging
4. **Additional Tools** - add `list_options`, `create_env`, `switch_env`
5. **Error Handling** - graceful fallbacks and user guidance

### Phase 3: UI Layer
1. **Overlay Window** - build GTK/QT prompt interface
2. **Global Shortcuts** - system-wide hotkey integration
3. **Agent Integration** - connect UI to existing shell agent
4. **ChatGPT Integration** - add API routing for general prompts
5. **App Launcher** - implement file and application opening tools

## GENERAL TASKS
- Define and document all agent tools with clear interfaces.
- Set up configuration files for environment recipes.
- Build logging system for debugging and user review.
- Develop installer or setup script for easy Raspberry Pi deployment.
- Write user instructions and a clear demo guide.

---

*This document describes the development plan for **CognOS**, an AI-driven operating system layer for Raspberry Pi that uses Mistral 7B on llama.cpp for local CLI-level automation and integrates with the ChatGPT API for general-purpose prompts.*