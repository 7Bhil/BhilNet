"""Gestion des messages pour BhilNet.

Développé par Bhilal CHITOU (Bhil€)
"""

import time
import threading
import logging
from typing import Dict, List, Optional
from utils import ThreadSafeDict

logger = logging.getLogger(__name__)

class MessageManager:
    """Handles message storage and processing."""
    
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.message_history = ThreadSafeDict()
        self.group_messages = []
        self.group_lock = threading.Lock()
    
    def add_private_message(self, sender_ip: str, sender_username: str, content: str):
        """Add a private message to history."""
        message_id = f"private_{int(time.time() * 1000)}"
        message = {
            'id': message_id,
            'type': 'private',
            'sender_ip': sender_ip,
            'sender_username': sender_username,
            'content': content,
            'timestamp': time.time()
        }
        
        if not self.message_history.get(sender_ip):
            self.message_history.set(sender_ip, [])
        
        user_messages = self.message_history.get(sender_ip)
        user_messages.append(message)
        
        # Keep only last max_history messages per user
        if len(user_messages) > self.max_history:
            user_messages = user_messages[-self.max_history:]
            self.message_history.set(sender_ip, user_messages)
        
        logger.info(f"Private message from {sender_username} ({sender_ip})")
    
    def add_group_message(self, sender_ip: str, sender_username: str, content: str):
        """Add a group message to history."""
        with self.group_lock:
            message = {
                'id': f"group_{int(time.time() * 1000)}",
                'type': 'group',
                'sender_ip': sender_ip,
                'sender_username': sender_username,
                'content': content,
                'timestamp': time.time()
            }
            
            self.group_messages.append(message)
            
            # Keep only last max_history group messages
            if len(self.group_messages) > self.max_history:
                self.group_messages = self.group_messages[-self.max_history:]
        
        logger.info(f"Group message from {sender_username} ({sender_ip})")
    
    def get_private_messages(self, user_ip: str) -> List[Dict]:
        """Get private message history with a specific user."""
        messages = self.message_history.get(user_ip, [])
        return sorted(messages, key=lambda x: x['timestamp'])
    
    def get_group_messages(self, limit: int = 20) -> List[Dict]:
        """Get recent group messages."""
        with self.group_lock:
            return sorted(self.group_messages, key=lambda x: x['timestamp'])[-limit:]
    
    def clear_history(self, user_ip: Optional[str] = None):
        """Clear message history."""
        if user_ip:
            self.message_history.delete(user_ip)
        else:
            self.message_history.clear()
            with self.group_lock:
                self.group_messages.clear()
    
    def format_message(self, message: Dict) -> str:
        """Format a message for display."""
        timestamp = time.strftime("%H:%M:%S", time.localtime(message['timestamp']))
        
        if message['type'] == 'private':
            return f"[{timestamp}] [Privé] {message['sender_username']}: {message['content']}"
        else:
            return f"[{timestamp}] [Groupe] {message['sender_username']}: {message['content']}"
