# Contributing to BhilNet

Thank you for your interest in contributing to BhilNet! This document provides guidelines for contributors.

## Getting Started

### Prerequisites
- Python 3.8+
- Git
- Basic understanding of networking concepts

### Setup Development Environment

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/yourusername/bhilnet.git
cd bhilnet
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
```

4. Install dependencies:
```bash
pip install -r requirements.txt
pip install -e .  # Install in development mode
```

## Development Guidelines

### Code Style
- Follow PEP 8 style guidelines
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use type hints where appropriate

### Code Structure
```
bhilnet/
├── main.py              # Entry point
├── utils/               # Utility functions
├── discovery/           # User discovery service
├── network/            # Network communication
├── messaging/          # Message handling
├── ui/                 # Terminal interface
├── crypto/             # Encryption utilities
└── tests/              # Test files
```

### Adding New Features

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Implement your changes following the existing patterns
3. Add tests for new functionality
4. Update documentation
5. Submit a pull request

### Testing

Before submitting, ensure:
- All existing tests pass
- New tests are added for new features
- Manual testing confirms functionality

```bash
# Run tests
python -m pytest tests/

# Manual test
python main.py
```

## Areas for Contribution

### High Priority
- [ ] Unit tests for all modules
- [ ] Configuration file support
- [ ] Better error handling
- [ ] Windows/macOS compatibility

### Medium Priority
- [ ] File sharing capability
- [ ] Voice chat support
- [ ] Message search functionality
- [ ] User profiles/avatars

### Low Priority
- [ ] GUI interface
- [ ] Web interface
- [ ] Mobile app
- [ ] Cloud synchronization

## Submitting Changes

### Pull Request Process

1. Update documentation
2. Ensure all tests pass
3. Update CHANGELOG.md
4. Submit pull request with:
   - Clear title
   - Detailed description
   - Testing instructions

### Code Review

All contributions require code review. Reviewers will check:
- Functionality
- Code quality
- Security implications
- Performance impact

## Bug Reports

When reporting bugs, include:
- Python version
- Operating system
- Network environment
- Steps to reproduce
- Error messages
- Logs (if applicable)

## Security

If you discover security vulnerabilities:
1. Do not open public issues
2. Email security@bhilnet.com
3. Wait for acknowledgment before disclosure

## Community

- Join our Discord server
- Participate in discussions
- Help other users
- Share ideas and feedback

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
