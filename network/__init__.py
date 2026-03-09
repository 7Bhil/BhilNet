"""Network communication module for BhilNet."""

import socket
import threading
import json
import time
import logging
from typing import Callable, Optional, Dict
from crypto import CryptoManager

logger = logging.getLogger(__name__)

class NetworkManager:
    """Handles TCP communication for messaging."""
    
    def __init__(self, username: str, port: int = 5002, encryption: bool = True):
        self.username = username
        self.port = port
        self.local_ip = "0.0.0.0"
        self.running = False
        self.server_socket = None
        self.on_message_received: Optional[Callable] = None
        self.crypto = CryptoManager() if encryption else None
    
    def start(self):
        """Start the TCP server."""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.local_ip, self.port))
        self.server_socket.listen(5)
        
        threading.Thread(target=self._accept_connections, daemon=True).start()
        logger.info(f"Network server started on port {self.port}")
    
    def stop(self):
        """Stop the TCP server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        logger.info("Network server stopped")
    
    def _accept_connections(self):
        """Accept incoming connections."""
        while self.running:
            try:
                self.server_socket.settimeout(1)
                client_socket, addr = self.server_socket.accept()
                threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, addr),
                    daemon=True
                ).start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    logger.error(f"Error accepting connection: {e}")
    
    def _handle_client(self, client_socket: socket.socket, addr: tuple):
        """Handle incoming messages from a client."""
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    message = json.loads(data.decode())
                    self._process_message(message, addr[0])
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON received from {addr[0]}")
                
        except Exception as e:
            logger.error(f"Error handling client {addr[0]}: {e}")
        finally:
            client_socket.close()
    
    def _process_message(self, message: dict, sender_ip: str):
        """Process received message."""
        if self.crypto and message.get('encrypted'):
            try:
                decrypted_content = self.crypto.decrypt(message['content'])
                message['content'] = decrypted_content
                message['encrypted'] = False
            except Exception:
                message['content'] = "[DECRYPT_ERROR]"
        
        message['sender_ip'] = sender_ip
        
        if self.on_message_received:
            self.on_message_received(message)
    
    def send_message(self, target_ip: str, content: str, message_type: str = "private") -> bool:
        """Send a message to a specific user."""
        try:
            message = {
                'type': message_type,
                'sender': self.username,
                'content': content,
                'timestamp': time.time()
            }
            
            if self.crypto:
                message['content'] = self.crypto.encrypt(content)
                message['encrypted'] = True
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(5)
            client_socket.connect((target_ip, self.port))
            
            client_socket.send(json.dumps(message).encode())
            client_socket.close()
            
            logger.info(f"Message sent to {target_ip}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending message to {target_ip}: {e}")
            return False
    
    def broadcast_message(self, content: str) -> bool:
        """Send a broadcast message to all users."""
        # This would need access to user list from discovery module
        # For now, return True as placeholder
        logger.info("Broadcast message functionality to be implemented")
        return True
