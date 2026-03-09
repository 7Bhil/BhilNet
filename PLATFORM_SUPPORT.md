# Platform Support Guide

## Current Status

BhilNet is primarily developed for Linux but can work on Windows and macOS with some considerations.

## Windows Support

### Requirements
- Python 3.8+ (64-bit recommended)
- Windows 10/11
- Network access

### Installation Steps
1. Download Python from python.org
2. During installation, check "Add Python to PATH"
3. Open Command Prompt as Administrator
4. Install dependencies:
```cmd
pip install -r requirements.txt
```
5. Run the application:
```cmd
python main.py
```

### Windows-Specific Issues

#### Firewall Prompts
Windows will likely show firewall prompts when BhilNet starts:
- Select "Private networks" for home/office use
- Click "Allow access" for both UDP and TCP

#### Network Discovery
Windows may have stricter network discovery:
- Ensure all machines are on the same "Private" network profile
- Check that Network Discovery is enabled in Windows settings

#### Administrator Rights
Some Windows configurations may require admin rights:
- Right-click Command Prompt → "Run as administrator"
- This is usually only needed for the first run

## macOS Support

### Requirements
- Python 3.8+ (comes pre-installed on recent macOS)
- macOS 10.14 Mojave or later
- Network access

### Installation Steps
1. Open Terminal (Applications → Utilities → Terminal)
2. Install dependencies:
```bash
pip3 install -r requirements.txt
```
3. Run the application:
```bash
python3 main.py
```

### macOS-Specific Issues

#### Security Prompts
macOS may show security prompts:
- Click "Allow" when prompted about network access
- If blocked, go to System Preferences → Security & Privacy → Privacy
- Add Terminal or Python to "Full Disk Access" if needed

#### Network Discovery
macOS network discovery works well but:
- Ensure Firewall allows Python (System Preferences → Security & Privacy → Firewall)
- Use "Automatically allow signed software" option

## Testing Cross-Platform

### Single Machine Testing
You can test multiple instances on one machine:
```bash
# Terminal 1
python main.py

# Terminal 2  
python main.py
```

### Network Testing
1. Ensure all machines can ping each other:
```bash
# Linux/macOS
ping 192.168.1.10

# Windows
ping 192.168.1.10
```

2. Check if ports are available:
```bash
# Linux/macOS
netstat -uln | grep 5000
netstat -tln | grep 5002

# Windows
netstat -an | findstr 5000
netstat -an | findstr 5002
```

## Platform-Specific Features

### Linux
- Full feature support
- Best performance
- Native terminal colors
- Automatic network detection

### Windows
- Full feature support
- May need admin rights for first run
- Command Prompt colors limited
- Network discovery may be slower

### macOS
- Full feature support
- Excellent terminal colors
- May need security permissions
- Good network discovery

## Troubleshooting by Platform

### Linux Issues
- Check firewall: `sudo ufw status`
- Check permissions: `ls -la /dev/log`
- Check network: `ip route show`

### Windows Issues
- Firewall: Windows Defender Firewall settings
- Network: Check network profile (Private vs Public)
- Python: Ensure PATH includes Python directory

### macOS Issues
- Security: System Preferences → Security & Privacy
- Firewall: System Preferences → Security & Privacy → Firewall
- Python: Use `python3` instead of `python`

## Future Platform Support

Planned improvements:
- [ ] Native Windows installer (.exe)
- [ ] macOS app bundle (.app)
- [ ] Better Windows firewall integration
- [ ] macOS notarization
- [ ] Cross-platform auto-updater
