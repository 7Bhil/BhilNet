"""Cross-platform compatibility utilities for BhilNet."""

import platform
import subprocess
import sys
import os

def clear_screen():
    """Clear terminal screen cross-platform."""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def get_broadcast_address():
    """Get broadcast address for the current network."""
    system = platform.system()
    
    if system == "Windows":
        # Windows specific broadcast detection
        try:
            result = subprocess.run(
                ["ipconfig", "/all"], 
                capture_output=True, 
                text=True, 
                shell=True
            )
            # Parse output to find broadcast address
            for line in result.stdout.split('\n'):
                if 'Subnet Mask' in line and '255.255.255.0' in line:
                    # Simple logic for /24 networks
                    return "255.255.255.255"
        except:
            pass
    else:
        # Linux/macOS
        try:
            result = subprocess.run(
                ["ip", "route", "show", "0.0.0.0/0"], 
                capture_output=True, 
                text=True
            )
            for line in result.stdout.split('\n'):
                if 'dev' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'src' and i + 1 < len(parts):
                            ip = parts[i + 1]
                            # Convert to broadcast for /24
                            return '.'.join(ip.split('.')[:-1] + ['255'])
        except:
            pass
    
    return "255.255.255.255"  # Fallback

def check_firewall_permission():
    """Check if we have permission to use network sockets."""
    try:
        import socket
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_socket.bind(('', 0))
        test_socket.close()
        return True
    except:
        return False

def get_platform_info():
    """Get platform information for debugging."""
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'python': platform.python_version(),
        'architecture': platform.architecture()[0]
    }

def setup_platform_specific():
    """Setup platform-specific configurations."""
    system = platform.system()
    
    if system == "Windows":
        # Windows-specific setup
        import socket
        # Allow socket reuse on Windows
        socket.SO_REUSEPORT = socket.SO_REUSEADDR
        
    elif system == "Darwin":  # macOS
        # macOS-specific setup
        pass
        
    elif system == "Linux":
        # Linux-specific setup
        pass
