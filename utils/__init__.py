"""Utility functions for BhilNet."""

import logging
import socket
import threading
from typing import Optional

def get_local_ip() -> str:
    """Get the local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def setup_logging(level: int = logging.INFO) -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('bhilnet.log'),
            logging.StreamHandler()
        ]
    )

class ThreadSafeDict:
    """Thread-safe dictionary for user management."""
    
    def __init__(self):
        self._dict = {}
        self._lock = threading.Lock()
    
    def get(self, key, default=None):
        with self._lock:
            return self._dict.get(key, default)
    
    def set(self, key, value):
        with self._lock:
            self._dict[key] = value
    
    def delete(self, key):
        with self._lock:
            if key in self._dict:
                del self._dict[key]
    
    def items(self):
        with self._lock:
            return list(self._dict.items())
    
    def clear(self):
        with self._lock:
            self._dict.clear()
