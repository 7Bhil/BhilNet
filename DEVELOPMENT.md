# Development Guide for BhilNet

## 🚀 Quick Start

### Automated Setup
```bash
./setup_dev.sh
```

### Manual Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 📦 Environment Setup

### Virtual Environment
Always use a virtual environment for development:

```bash
# Create
python3 -m venv venv

# Activate
source venv/bin/activate

# Deactivate when done
deactivate
```

### Dependencies
Install all required packages:
```bash
pip install -r requirements.txt
```

For development, also install:
```bash
pip install pytest black flake8 mypy
```

## 🔧 Development Workflow

### 1. Make Changes
- Edit source files
- Test locally with `python main.py`

### 2. Run Tests
```bash
python -m pytest tests/
```

### 3. Code Quality
```bash
# Format code
black *.py

# Check style
flake8 *.py

# Type checking
mypy *.py
```

### 4. Commit Changes
```bash
git add .
git commit -m "Your descriptive message"
git push
```

## 🏗️ Project Structure

```
BhilNet/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── setup_dev.sh        # Dev setup script
├── venv/               # Virtual environment (gitignored)
├── utils/              # Utility functions
├── discovery/          # User discovery
├── network/           # Network communication
├── messaging/         # Message handling
├── ui/                # Terminal interface
├── crypto/            # Encryption
├── config_manager.py  # Configuration
├── sound_manager.py   # Sound notifications
├── user_status.py     # User status management
├── cross_platform.py  # Platform compatibility
├── logs/              # Log files (gitignored)
├── bhilnet.log        # Application log (gitignored)
├── bhilnet_config.json # User config (gitignored)
└── tests/             # Unit tests
```

## 🐛 Debugging

### Enable Debug Mode
```bash
export BHILNET_DEBUG=1
python main.py
```

### Check Logs
```bash
tail -f bhilnet.log
```

### Network Issues
```bash
# Check if ports are in use
netstat -tlnp | grep 5002
netstat -ulnp | grep 5000

# Test network connectivity
ping -b 255.255.255.255
```

## 🧪 Testing

### Unit Tests
```bash
python -m pytest tests/ -v
```

### Integration Tests
```bash
# Test with multiple terminals
# Terminal 1:
python main.py

# Terminal 2:
python main.py
```

### Manual Testing Checklist
- [ ] User discovery works
- [ ] Private messages send/receive
- [ ] Group messages send/receive
- [ ] Status changes work
- [ ] Sound notifications work
- [ ] Configuration persists
- [ ] Quick messages expand
- [ ] Auto-away activates

## 📝 Code Style

### Python Standards
- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Use f-strings for formatting

### Example Code Style
```python
def send_message(self, target_ip: str, content: str) -> bool:
    """Send a message to target user.
    
    Args:
        target_ip: IP address of recipient
        content: Message content to send
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Implementation here
        return True
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return False
```

## 🔍 Common Issues

### Port Already in Use
```bash
# Find process using port
sudo lsof -i :5002
sudo lsof -i :5000

# Kill process
sudo kill -9 <PID>
```

### Permission Denied
```bash
# Check file permissions
ls -la bhilnet.log

# Fix permissions
chmod 666 bhilnet.log
```

### Virtual Environment Issues
```bash
# Recreate environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Deployment

### Create Package
```bash
python setup.py sdist bdist_wheel
```

### Install Package
```bash
pip install dist/bhilnet-1.0.0-py3-none-any.whl
```

### Run Installed Package
```bash
bhilnet
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📚 Resources

- [Python Virtual Environments](https://docs.python.org/3/library/venv.html)
- [PEP 8 Style Guide](https://pep8.org/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Git Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows)
