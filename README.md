# BhilNet - LAN Terminal Chat

A terminal-based messaging application for local network communication.

## Features

- Automatic user discovery via UDP broadcast
- Private and group messaging via TCP
- Real-time user list updates
- AES message encryption
- Clean terminal interface
- Multi-threaded architecture

## Installation

```bash
pip install -r requirements.txt
python main.py
```

## Platform Support

- **Linux** ✅ - Fully supported and tested
- **Windows** ⚠️ - Supported with minor modifications
- **macOS** ⚠️ - Supported with minor modifications

### Windows/macOS Setup

1. Install Python 3.8+ from python.org
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`

For Windows users, you may need to:
- Allow Python through Windows Firewall
- Run Command Prompt as Administrator if needed

## Usage

1. Run the application on multiple machines in the same LAN
2. Choose a username when prompted
3. View connected users and send messages

## Architecture

- `main.py` - Entry point and main application
- `network/` - Network communication modules
- `discovery/` - User discovery service
- `messaging/` - Message handling
- `ui/` - Terminal interface
- `crypto/` - Encryption utilities
- `utils/` - Helper functions

## Requirements

- Python 3.8+
- Linux operating system
- Local network access
