"""User discovery service for BhilNet."""

import socket
import threading
import time
import json
import logging
from typing import Dict, Callable, Optional
from utils import get_local_ip, ThreadSafeDict

logger = logging.getLogger(__name__)

class UserDiscovery:
    """Handles user discovery via UDP broadcast."""
    
    def __init__(self, username: str, port: int = 5001):
        self.username = username
        self.local_ip = get_local_ip()
        self.port = port
        self.broadcast_port = 5000
        self.users = ThreadSafeDict()
        self.running = False
        self.on_user_joined: Optional[Callable] = None
        self.on_user_left: Optional[Callable] = None
        
        # Add self to users list
        self.users.set(self.local_ip, {
            'username': username,
            'ip': self.local_ip,
            'last_seen': time.time()
        })
    
    def start(self):
        """Start the discovery service."""
        self.running = True
        threading.Thread(target=self._broadcast_presence, daemon=True).start()
        threading.Thread(target=self._listen_for_broadcasts, daemon=True).start()
        threading.Thread(target=self._cleanup_inactive_users, daemon=True).start()
        logger.info(f"User discovery started for {self.username} at {self.local_ip}")
    
    def stop(self):
        """Stop the discovery service."""
        self.running = False
        self._broadcast_goodbye()
        logger.info("User discovery stopped")
    
    def _broadcast_presence(self):
        """Broadcast presence every 5 seconds."""
        while self.running:
            try:
                message = {
                    'type': 'presence',
                    'username': self.username,
                    'ip': self.local_ip,
                    'timestamp': time.time()
                }
                self._send_broadcast(message)
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error broadcasting presence: {e}")
    
    def _broadcast_goodbye(self):
        """Broadcast goodbye message when leaving."""
        try:
            message = {
                'type': 'goodbye',
                'username': self.username,
                'ip': self.local_ip,
                'timestamp': time.time()
            }
            self._send_broadcast(message)
        except Exception as e:
            logger.error(f"Error broadcasting goodbye: {e}")
    
    def _send_broadcast(self, message: Dict):
        """Send UDP broadcast message."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(1)
        
        try:
            sock.sendto(
                json.dumps(message).encode(),
                ('<broadcast>', self.broadcast_port)
            )
        except Exception as e:
            logger.error(f"Error sending broadcast: {e}")
        finally:
            sock.close()
    
    def _listen_for_broadcasts(self):
        """Listen for broadcast messages from other users."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.broadcast_port))
        sock.settimeout(1)
        
        while self.running:
            try:
                data, addr = sock.recvfrom(1024)
                message = json.loads(data.decode())
                self._handle_broadcast_message(message, addr[0])
            except socket.timeout:
                continue
            except Exception as e:
                logger.error(f"Error receiving broadcast: {e}")
        
        sock.close()
    
    def _handle_broadcast_message(self, message: Dict, sender_ip: str):
        """Handle incoming broadcast messages."""
        if sender_ip == self.local_ip:
            return  # Ignore own messages
        
        msg_type = message.get('type')
        username = message.get('username')
        
        if msg_type == 'presence':
            user_info = {
                'username': username,
                'ip': sender_ip,
                'last_seen': time.time()
            }
            self.users.set(sender_ip, user_info)
            
            if self.on_user_joined:
                self.on_user_joined(user_info)
                
        elif msg_type == 'goodbye':
            if self.users.get(sender_ip):
                user_info = self.users.get(sender_ip)
                self.users.delete(sender_ip)
                
                if self.on_user_left:
                    self.on_user_left(user_info)
    
    def _cleanup_inactive_users(self):
        """Remove users that haven't been seen for 15 seconds."""
        while self.running:
            try:
                current_time = time.time()
                for ip, user_info in self.users.items():
                    if current_time - user_info['last_seen'] > 15:
                        self.users.delete(ip)
                        if self.on_user_left:
                            self.on_user_left(user_info)
                time.sleep(5)
            except Exception as e:
                logger.error(f"Error cleaning up inactive users: {e}")
    
    def get_users(self) -> Dict[str, Dict]:
        """Get all active users except self."""
        users = self.users.items()
        return {ip: info for ip, info in users if ip != self.local_ip}
