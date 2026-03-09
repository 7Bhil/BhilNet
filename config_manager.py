"""Configuration management for BhilNet."""

import json
import os
from typing import Dict, Any

class ConfigManager:
    """Manages application configuration."""
    
    def __init__(self, config_file: str = "bhilnet_config.json"):
        self.config_file = config_file
        self.default_config = {
            "username": "",
            "encryption_enabled": True,
            "notification_sound": False,
            "auto_refresh_interval": 5,
            "theme": "default",
            "max_history": 100,
            "default_status": "online",
            "quick_messages": {
                ":hi": "Hello everyone!",
                ":bye": "Goodbye!",
                ":brb": "Be right back",
                ":coffee": "Going for coffee ☕"
            }
        }
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                config = self.default_config.copy()
                config.update(loaded_config)
                return config
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return self.default_config.copy()
    
    def save_config(self) -> bool:
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """Set configuration value."""
        self.config[key] = value
        return self.save_config()
    
    def get_quick_message(self, shortcut: str) -> str:
        """Get quick message by shortcut."""
        return self.config.get("quick_messages", {}).get(shortcut, "")
    
    def add_quick_message(self, shortcut: str, message: str) -> bool:
        """Add a quick message."""
        if "quick_messages" not in self.config:
            self.config["quick_messages"] = {}
        self.config["quick_messages"][shortcut] = message
        return self.save_config()
