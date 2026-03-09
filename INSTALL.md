# Installation Guide for BhilNet

## Prerequisites

- Python 3.8 or higher
- Linux operating system
- Network access (local LAN)

## Installation Methods

### Method 1: From Source (Recommended)

1. Clone or download the BhilNet source code:
```bash
git clone https://github.com/bhilnet/bhilnet.git
cd bhilnet
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

### Method 2: Using pip (if published)

```bash
pip install bhilnet
bhilnet
```

### Method 3: Using setup.py

```bash
python setup.py install
bhilnet
```

## Network Configuration

### Firewall Configuration

BhilNet uses the following ports:
- **UDP 5000**: User discovery (broadcast)
- **TCP 5002**: Message communication

Make sure these ports are open in your firewall:

```bash
# For ufw (Ubuntu/Debian)
sudo ufw allow 5000/udp
sudo ufw allow 5002/tcp

# For firewalld (Fedora/CentOS)
sudo firewall-cmd --add-port=5000/udp --permanent
sudo firewall-cmd --add-port=5002/tcp --permanent
sudo firewall-cmd --reload

# For iptables
sudo iptables -A INPUT -p udp --dport 5000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 5002 -j ACCEPT
```

### Network Requirements

- All users must be on the same local network (LAN)
- UDP broadcast must be enabled on the network
- No VPN or proxy interference

## Testing the Installation

1. Install BhilNet on at least two machines on the same network
2. Run the application on both machines:
```bash
python main.py
```
3. Choose different usernames on each machine
4. Verify that users appear in each other's user lists
5. Test sending private and group messages

## Troubleshooting

### Users not appearing

1. Check firewall settings
2. Verify all machines are on the same network
3. Check if UDP broadcast is blocked by network equipment
4. Run with logging enabled:
```bash
python main.py 2>&1 | tee bhilnet.log
```

### Messages not sending

1. Verify TCP port 5002 is open
2. Check if target machine is running BhilNet
3. Look at the log file for error messages

### Permission errors

1. Make sure Python has network permissions
2. Try running as user (not root) first
3. If needed, use sudo only for testing

## Uninstallation

### If installed via pip:
```bash
pip uninstall bhilnet
```

### If installed from source:
```bash
# Remove the source directory
rm -rf bhilnet
```

## Support

For issues and support:
- Check the log file: `bhilnet.log`
- Verify network connectivity
- Ensure all prerequisites are met
