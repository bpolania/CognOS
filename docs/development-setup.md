# CognOS Development Setup

## Overview

CognOS is designed to run on Raspberry Pi as the target platform. This guide covers setting up a development environment using VS Code Remote SSH for the best developer experience - combining laptop editor comfort with Pi execution environment.

## Prerequisites

### Raspberry Pi Requirements
- Raspberry Pi 5 with 8GB RAM (recommended) or Raspberry Pi 4 with 8GB RAM
- Raspberry Pi OS (64-bit) installed
- SSH enabled
- Internet connection
- At least 16GB storage available

**Note:** Raspberry Pi 5 is fully supported and will provide better performance than Pi 4, especially for AI model inference.

### Development Machine Requirements (Mac)
- VS Code installed
- Git configured (comes pre-installed on macOS)
- SSH client (built-in on macOS)
- Xcode Command Line Tools (if not already installed): `xcode-select --install`

## Setup Process

### 1. Raspberry Pi Initial Setup

**Enable SSH on Pi:**
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

**Find Pi IP address:**
```bash
hostname -I
```

**Update system:**
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. VS Code Remote SSH Setup

**Install Remote SSH extension:**
1. Open VS Code
2. Go to Extensions (Cmd+Shift+X)
3. Search for "Remote - SSH"
4. Install the extension by Microsoft

**Configure SSH connection:**
1. Press `Cmd+Shift+P` and type "Remote-SSH: Connect to Host"
2. Select "Add New SSH Host"
3. Enter: `ssh pi@<pi-ip-address>`
4. Choose SSH config file to save to (usually `~/.ssh/config`)

**Connect to Pi:**
1. Press `Cmd+Shift+P` and type "Remote-SSH: Connect to Host"
2. Select your Pi from the list
3. Enter password when prompted
4. VS Code will install the remote server on Pi

### 3. Clone and Setup CognOS

**In VS Code connected to Pi:**

**Open terminal in VS Code (Cmd+`):**
```bash
# Clone the repository
git clone <your-repo-url>
cd CognOS
```

**Install dependencies:**
```bash
make setup
```

**Download AI models:**
```bash
make models
```

**Verify setup:**
```bash
# Check Python environment
source venv/bin/activate
python3 --version
pip list | grep llama

# Check project structure
ls -la src/
```

### 4. Development Workflow

**Daily development process:**

1. **Connect to Pi:**
   - Open VS Code
   - Connect to Pi via Remote SSH
   - Open CognOS folder

2. **Activate environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Make changes:**
   - Edit files directly in VS Code
   - Files are automatically saved on Pi
   - Use VS Code's integrated terminal for commands

4. **Test changes:**
   ```bash
   # Test individual components
   python3 src/agent/main.py "show me files"
   python3 src/shell/main.py
   
   # Run tests
   make test
   ```

5. **Build and install:**
   ```bash
   make build
   make install
   ```

6. **Test as default shell:**
   ```bash
   # Test without changing default
   /usr/local/bin/cognos-shell
   
   # Set as default shell (optional)
   chsh -s /usr/local/bin/cognos-shell
   ```

### 5. Development Tips

**VS Code Remote Features:**
- File explorer works directly on Pi filesystem
- Integrated terminal runs commands on Pi
- Extensions install on Pi automatically
- Git integration works seamlessly
- Debugging works with Pi Python environment

**Useful VS Code Extensions for Pi development:**
- Python
- GitLens
- Thunder Client (for API testing)
- YAML
- Makefile Tools

**Terminal shortcuts:**
```bash
# Quick restart of shell service
sudo systemctl restart cognos-shell

# Check logs
tail -f ~/.local/share/cognos/cognos.log

# Monitor system resources
htop

# Check model loading
ls -la models/
```

### 6. Troubleshooting

**SSH Connection Issues:**
- Verify Pi IP address: `hostname -I`
- Check SSH service: `sudo systemctl status ssh`
- Test connection: `ssh pi@<pi-ip>` from Mac terminal

**Performance Issues:**
- Monitor Pi resources: `htop`
- Check model size: `ls -lh models/`
- Verify swap: `free -h`

**Python Environment Issues:**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Model Loading Issues:**
```bash
# Re-download models
rm -rf models/*.gguf
make models
```

## Advanced Configuration

### Custom SSH Config

**Edit `~/.ssh/config` on your Mac:**
```
Host cognos-pi
    HostName <pi-ip-address>
    User pi
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

### VS Code Settings for Pi Development

**Add to VS Code settings.json:**
```json
{
    "remote.SSH.remotePlatform": {
        "cognos-pi": "linux"
    },
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true
}
```

## Security Considerations

- Use SSH keys instead of passwords for better security
- Keep Pi OS updated regularly
- Use firewall rules to restrict access
- Regular backups of development work

## Next Steps

Once development environment is set up:
1. Begin Phase 1 development (llama.cpp integration)
2. Test natural language command processing
3. Implement core filesystem tools
4. Verify shell replacement functionality

This setup provides the optimal development experience for CognOS on Raspberry Pi while maintaining the comfort of laptop-based development tools.