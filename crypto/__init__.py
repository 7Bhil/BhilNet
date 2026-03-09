"""Encryption utilities for BhilNet."""

import os
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class CryptoManager:
    """Handles encryption and decryption of messages."""
    
    def __init__(self, password: str = "bhilnet_default"):
        self.password = password.encode()
        self.salt = os.urandom(16)
        self.key = self._derive_key()
        self.cipher = Fernet(self.key)
    
    def _derive_key(self) -> bytes:
        """Derive encryption key from password."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.password))
        return key
    
    def encrypt(self, message: str) -> str:
        """Encrypt a message."""
        encrypted = self.cipher.encrypt(message.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_message: str) -> str:
        """Decrypt a message."""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_message.encode())
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode()
        except Exception:
            return "[DECRYPT_ERROR]"
    
    @staticmethod
    def generate_key() -> str:
        """Generate a new encryption key."""
        return base64.urlsafe_b64encode(Fernet.generate_key()).decode()
