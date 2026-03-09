# Testing Guide for BhilNet

## Quick Start Testing

### Single Machine Testing (Multiple Terminals)

1. Open multiple terminal windows on the same machine
2. In each terminal, run:
```bash
cd /path/to/bhilnet
python main.py
```
3. Choose different usernames in each terminal
4. Test the functionality

### Multi-Machine Testing

1. Install BhilNet on at least 2 machines on the same LAN
2. Ensure both machines can ping each other
3. Run BhilNet on both machines
4. Verify user discovery and messaging

## Test Scenarios

### Test 1: User Discovery
- [ ] Launch BhilNet on machine A
- [ ] Launch BhilNet on machine B
- [ ] Verify B appears in A's user list
- [ ] Verify A appears in B's user list
- [ ] Close B and verify B disappears from A's list

### Test 2: Private Messaging
- [ ] Select a user from the list
- [ ] Send a private message
- [ ] Verify message appears on recipient's screen
- [ ] Send reply and verify bidirectional communication

### Test 3: Group Messaging
- [ ] Send a group message with 2+ users online
- [ ] Verify all users receive the message
- [ ] Test with only 1 user online

### Test 4: Message History
- [ ] Send several messages
- [ ] Check message history option
- [ ] Verify messages are stored correctly
- [ ] Test private vs group message separation

### Test 5: Connection Handling
- [ ] Test user joining/leaving notifications
- [ ] Test network disconnection/reconnection
- [ ] Test graceful shutdown with Ctrl+C

## Network Testing Commands

### Check Network Connectivity
```bash
# Ping another machine
ping 192.168.1.10

# Check if ports are listening
netstat -ulnp | grep 5000  # UDP discovery
netstat -tlnp | grep 5002  # TCP messaging

# Check firewall status
sudo ufw status
```

### Monitor Network Traffic
```bash
# Monitor UDP broadcasts
sudo tcpdump -i any udp port 5000

# Monitor TCP messages
sudo tcpdump -i any tcp port 5002
```

## Test Script

Create a test script to automate basic functionality:

```bash
#!/bin/bash
# test_bhilnet.sh

echo "BhilNet Test Script"
echo "=================="

# Test 1: Import modules
python -c "
try:
    from utils import get_local_ip
    from discovery import UserDiscovery
    from network import NetworkManager
    from messaging import MessageManager
    from ui import TerminalUI
    print('✓ All modules imported successfully')
except Exception as e:
    print(f'✗ Import error: {e}')
    exit(1)
"

# Test 2: Network utilities
python -c "
from utils import get_local_ip
ip = get_local_ip()
print(f'✓ Local IP detected: {ip}')
if ip == '127.0.0.1':
    print('⚠ Warning: Could not detect real IP address')
"

# Test 3: Crypto functionality
python -c "
from crypto import CryptoManager
crypto = CryptoManager()
test_msg = 'Hello, BhilNet!'
encrypted = crypto.encrypt(test_msg)
decrypted = crypto.decrypt(encrypted)
if decrypted == test_msg:
    print('✓ Encryption/decryption working')
else:
    print('✗ Encryption test failed')
"

echo "Basic tests completed."
```

## Debug Mode

Run BhilNet with debug logging:

```bash
export BHILNET_DEBUG=1
python main.py 2>&1 | tee bhilnet_debug.log
```

## Common Issues and Solutions

### Issue: Users not discovered
**Symptoms**: No other users appear in the list
**Causes**: 
- Firewall blocking UDP port 5000
- Network equipment blocking broadcasts
- Different subnets

**Solutions**:
```bash
# Temporarily disable firewall for testing
sudo ufw disable

# Check broadcast capability
ping -b 255.255.255.255
```

### Issue: Messages not sending
**Symptoms**: Message appears sent but not received
**Causes**:
- Firewall blocking TCP port 5002
- Target application not running
- Network routing issues

**Solutions**:
```bash
# Check if port is open
telnet target_ip 5002

# Check application logs
tail -f bhilnet.log
```

### Issue: Permission errors
**Symptoms**: "Permission denied" errors
**Causes**:
- Python sandbox restrictions
- Network permissions

**Solutions**:
```bash
# Run as regular user (recommended)
python main.py

# Only use sudo if necessary
sudo python main.py
```

## Performance Testing

### Load Testing
Test with multiple simultaneous users:
```bash
# Simulate 10 users (requires multiple terminals or machines)
for i in {1..10}; do
    gnome-terminal -- python main.py &
done
```

### Memory Usage
Monitor memory consumption:
```bash
# Monitor memory usage
python main.py &
PID=$!
while sleep 5; do
    ps -p $PID -o pid,ppid,cmd,%mem,%cpu --no-headers
done
```

## Automated Testing

For comprehensive testing, consider creating unit tests:

```python
# tests/test_bhilnet.py
import unittest
from utils import get_local_ip
from crypto import CryptoManager

class TestBhilNet(unittest.TestCase):
    def test_local_ip_detection(self):
        ip = get_local_ip()
        self.assertIsNotNone(ip)
        self.assertNotEqual(ip, "")
    
    def test_encryption(self):
        crypto = CryptoManager()
        message = "Test message"
        encrypted = crypto.encrypt(message)
        decrypted = crypto.decrypt(encrypted)
        self.assertEqual(message, decrypted)

if __name__ == '__main__':
    unittest.main()
```

Run tests with:
```bash
python -m pytest tests/
```
