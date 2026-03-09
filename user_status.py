"""User status management for BhilNet."""

import time
import threading
from enum import Enum
from typing import Dict, Optional

class UserStatus(Enum):
    """User status enumeration."""
    ONLINE = "online"
    AWAY = "away"
    BUSY = "busy"
    INVISIBLE = "invisible"

class StatusManager:
    """Manages user status and presence."""
    
    def __init__(self, auto_away_timeout: int = 300):  # 5 minutes
        self.current_status = UserStatus.ONLINE
        self.status_message = ""
        self.auto_away_timeout = auto_away_timeout
        self.last_activity = time.time()
        self.auto_away_enabled = True
        self.running = False
        self._lock = threading.Lock()
        
    def set_status(self, status: UserStatus, message: str = ""):
        """Set user status."""
        with self._lock:
            self.current_status = status
            self.status_message = message
            self.last_activity = time.time()
    
    def get_status(self) -> Dict[str, str]:
        """Get current status information."""
        with self._lock:
            return {
                "status": self.current_status.value,
                "message": self.status_message,
                "last_activity": self.last_activity
            }
    
    def update_activity(self):
        """Update last activity timestamp."""
        with self._lock:
            self.last_activity = time.time()
            # If user was auto-away, set back to online
            if self.current_status == UserStatus.AWAY and self.auto_away_enabled:
                self.current_status = UserStatus.ONLINE
    
    def start_auto_away_monitor(self):
        """Start the auto-away monitoring thread."""
        self.running = True
        threading.Thread(target=self._auto_away_monitor, daemon=True).start()
    
    def stop_auto_away_monitor(self):
        """Stop the auto-away monitoring thread."""
        self.running = False
    
    def _auto_away_monitor(self):
        """Monitor inactivity and set auto-away."""
        while self.running:
            time.sleep(30)  # Check every 30 seconds
            
            if not self.auto_away_enabled:
                continue
            
            with self._lock:
                current_time = time.time()
                inactive_time = current_time - self.last_activity
                
                if inactive_time >= self.auto_away_timeout:
                    if self.current_status == UserStatus.ONLINE:
                        self.current_status = UserStatus.AWAY
                        self.status_message = "Auto-away (inactive)"
    
    def enable_auto_away(self):
        """Enable auto-away functionality."""
        self.auto_away_enabled = True
    
    def disable_auto_away(self):
        """Disable auto-away functionality."""
        self.auto_away_enabled = False
    
    def set_auto_away_timeout(self, timeout_seconds: int):
        """Set auto-away timeout in seconds."""
        self.auto_away_timeout = timeout_seconds
    
    @staticmethod
    def get_status_emoji(status: UserStatus) -> str:
        """Get emoji representation of status."""
        emoji_map = {
            UserStatus.ONLINE: "🟢",
            UserStatus.AWAY: "🟡", 
            UserStatus.BUSY: "🔴",
            UserStatus.INVISIBLE: "⚫"
        }
        return emoji_map.get(status, "⚪")
    
    @staticmethod
    def get_status_color(status: UserStatus) -> str:
        """Get color representation for terminal display."""
        from colorama import Fore
        color_map = {
            UserStatus.ONLINE: Fore.GREEN,
            UserStatus.AWAY: Fore.YELLOW,
            UserStatus.BUSY: Fore.RED,
            UserStatus.INVISIBLE: Fore.LIGHTBLACK_EX
        }
        return color_map.get(status, Fore.WHITE)
