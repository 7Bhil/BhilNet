#!/usr/bin/env python3
"""BhilNet - LAN Terminal Chat Application."""

import sys
import signal
import threading
import time
import logging
from typing import Dict, List

# Import modules
from utils import setup_logging
from discovery import UserDiscovery
from network import NetworkManager
from messaging import MessageManager
from ui import TerminalUI
from config_manager import ConfigManager
from sound_manager import SoundManager
from user_status import StatusManager, UserStatus

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

class BhilNet:
    """Main application class for BhilNet."""
    
    def __init__(self):
        self.config = ConfigManager()
        self.ui = TerminalUI()
        self.sound = SoundManager(enabled=self.config.get("notification_sound", False))
        self.status_manager = StatusManager()
        self.username = ""
        self.discovery = None
        self.network = None
        self.messaging = None
        self.running = False
        self.incoming_messages = []
        self.message_lock = threading.Lock()
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully."""
        print(f"\n{'='*50}")
        print("Shutting down BhilNet...")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Start the BhilNet application."""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Get username (use saved one or ask)
        saved_username = self.config.get("username", "")
        self.username = self.ui.get_username(saved_username)
        
        # Save username for next time
        self.config.set("username", self.username)
        
        # Initialize modules
        self.discovery = UserDiscovery(self.username)
        self.network = NetworkManager(self.username, encryption=self.config.get("encryption_enabled", True))
        self.messaging = MessageManager(max_history=self.config.get("max_history", 100))
        
        # Setup callbacks
        self.discovery.on_user_joined = self.on_user_joined
        self.discovery.on_user_left = self.on_user_left
        self.network.on_message_received = self.on_message_received
        
        # Start services
        self.discovery.start()
        self.network.start()
        self.status_manager.start_auto_away_monitor()
        self.running = True
        
        # Start message display thread
        threading.Thread(target=self.message_display_thread, daemon=True).start()
        
        # Main loop
        self.main_loop()
    
    def stop(self):
        """Stop the BhilNet application."""
        self.running = False
        if self.status_manager:
            self.status_manager.stop_auto_away_monitor()
        if self.discovery:
            self.discovery.stop()
        if self.network:
            self.network.stop()
        self.ui.quit_screen()
    
    def main_loop(self):
        """Main application loop."""
        while self.running:
            try:
                # Update activity (prevents auto-away)
                self.status_manager.update_activity()
                
                # Get current users
                users = self.discovery.get_users()
                
                # Get recent messages
                recent_messages = self.get_recent_messages()
                
                # Get current status
                current_status = self.status_manager.get_status()
                
                # Show main interface
                self.ui.show_main_interface(users, recent_messages, current_status)
                
                # Get menu choice
                choice = self.ui.get_menu_choice()
                
                # Handle menu choice
                if choice == 1:
                    self.send_private_message()
                elif choice == 2:
                    self.send_group_message()
                elif choice == 3:
                    self.refresh_users()
                elif choice == 4:
                    self.change_status()
                elif choice == 5:
                    self.toggle_sound()
                elif choice == 6:
                    self.show_message_history()
                elif choice == 7:
                    self.show_settings()
                elif choice == 8:
                    self.stop()
                    break
                    
            except KeyboardInterrupt:
                self.stop()
                break
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(1)
    
    def send_private_message(self):
        """Send a private message."""
        users = self.discovery.get_users()
        target_ip = self.ui.select_user(users)
        
        if target_ip:
            message = self.ui.get_message("Enter your private message")
            if message:
                # Check for quick message shortcuts
                expanded_message = self.config.get_quick_message(message)
                if expanded_message:
                    message = expanded_message
                
                success = self.network.send_message(target_ip, message, "private")
                if success:
                    # Add to own message history
                    target_user = users[target_ip]
                    self.messaging.add_private_message(
                        target_ip, target_user['username'], 
                        f"You: {message}"
                    )
                    self.ui.show_notification("Message sent successfully!", Fore.GREEN)
                else:
                    self.ui.show_notification("Failed to send message!", Fore.RED)
    
    def send_group_message(self):
        """Send a group message to all users."""
        users = self.discovery.get_users()
        
        if not users:
            self.ui.show_notification("No users available for group message!", Fore.YELLOW)
            return
        
        message = self.ui.get_message("Enter your group message")
        if message:
            # Check for quick message shortcuts
            expanded_message = self.config.get_quick_message(message)
            if expanded_message:
                message = expanded_message
            
            # Send to each user
            sent_count = 0
            for user_ip in users:
                if self.network.send_message(user_ip, message, "group"):
                    sent_count += 1
            
            if sent_count > 0:
                # Add to own group message history
                self.messaging.add_group_message(
                    "self", self.username, 
                    f"You: {message}"
                )
                self.ui.show_notification(
                    f"Group message sent to {sent_count} user(s)!", 
                    Fore.GREEN
                )
            else:
                self.ui.show_notification("Failed to send group message!", Fore.RED)
    
    def change_status(self):
        """Change user status."""
        from user_status import UserStatus
        
        print(f"\n{Fore.BLUE}Select your status:{Style.RESET_ALL}")
        print("  1 - 🟢 Online")
        print("  2 - 🟡 Away")
        print("  3 - 🔴 Busy")
        print("  4 - ⚫ Invisible")
        print("  0 - Cancel")
        
        while True:
            try:
                choice = input(f"\n{Fore.CYAN}Enter status number: {Style.RESET_ALL}").strip()
                if choice == '0':
                    return
                
                status_map = {
                    '1': UserStatus.ONLINE,
                    '2': UserStatus.AWAY,
                    '3': UserStatus.BUSY,
                    '4': UserStatus.INVISIBLE
                }
                
                if choice in status_map:
                    status = status_map[choice]
                    message = input(f"{Fore.CYAN}Status message (optional): {Style.RESET_ALL}").strip()
                    
                    self.status_manager.set_status(status, message)
                    self.ui.show_notification(f"Status changed to {status.value}!", Fore.GREEN)
                    return
                
                print(f"{Fore.RED}Invalid choice! Please enter 0-4.{Style.RESET_ALL}")
                
            except (ValueError, KeyboardInterrupt):
                return
    
    def toggle_sound(self):
        """Toggle sound notifications."""
        current_state = self.sound.enabled
        new_state = not current_state
        
        if new_state:
            self.sound.enable()
            self.config.set("notification_sound", True)
            self.ui.show_notification("Sound notifications enabled!", Fore.GREEN)
        else:
            self.sound.disable()
            self.config.set("notification_sound", False)
            self.ui.show_notification("Sound notifications disabled!", Fore.YELLOW)
    
    def show_settings(self):
        """Show and edit settings."""
        print(f"\n{Fore.BLUE}Current Settings:{Style.RESET_ALL}")
        print(f"  Username: {self.config.get('username', 'Not set')}")
        print(f"  Encryption: {Fore.GREEN}ON{Style.RESET_ALL}" if self.config.get('encryption_enabled') else f"  Encryption: {Fore.RED}OFF{Style.RESET_ALL}")
        print(f"  Sound: {Fore.GREEN}ON{Style.RESET_ALL}" if self.config.get('notification_sound') else f"  Sound: {Fore.RED}OFF{Style.RESET_ALL}")
        print(f"  Max History: {self.config.get('max_history', 100)} messages")
        print(f"  Auto-away: {Fore.GREEN}ON{Style.RESET_ALL}" if self.status_manager.auto_away_enabled else f"  Auto-away: {Fore.RED}OFF{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Quick Messages:{Style.RESET_ALL}")
        quick_msgs = self.config.get("quick_messages", {})
        for shortcut, message in quick_msgs.items():
            print(f"  {shortcut} → {message}")
        
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def refresh_users(self):
        """Refresh the user list."""
        self.ui.show_notification("User list refreshed!", Fore.GREEN)
        time.sleep(1)
    
    def show_message_history(self):
        """Show message history."""
        private_messages = {}
        users = self.discovery.get_users()
        
        # Get private messages for each user
        for user_ip, user_info in users.items():
            messages = self.messaging.get_private_messages(user_ip)
            if messages:
                private_messages[user_ip] = messages
        
        group_messages = self.messaging.get_group_messages()
        
        # Format messages for display
        formatted_private = {}
        for user_ip, messages in private_messages.items():
            formatted_private[user_ip] = [
                self.messaging.format_message(msg) for msg in messages
            ]
        
        formatted_group = [
            self.messaging.format_message(msg) for msg in group_messages
        ]
        
        self.ui.show_message_history(formatted_private, formatted_group)
    
    def get_recent_messages(self) -> List[str]:
        """Get recent messages for display."""
        with self.message_lock:
            return self.incoming_messages[-5:]  # Return last 5 messages
    
    def on_user_joined(self, user_info: Dict):
        """Handle user joined event."""
        message = f"{user_info['username']} joined the chat"
        with self.message_lock:
            self.incoming_messages.append(f"[{time.strftime('%H:%M:%S')}] {Fore.GREEN}{message}{Style.RESET_ALL}")
        self.sound.play_notification("user_join")
    
    def on_user_left(self, user_info: Dict):
        """Handle user left event."""
        message = f"{user_info['username']} left the chat"
        with self.message_lock:
            self.incoming_messages.append(f"[{time.strftime('%H:%M:%S')}] {Fore.RED}{message}{Style.RESET_ALL}")
        self.sound.play_notification("user_leave")
    
    def on_message_received(self, message: Dict):
        """Handle incoming message."""
        sender_ip = message.get('sender_ip', 'Unknown')
        sender_name = message.get('sender', 'Unknown')
        content = message.get('content', '')
        msg_type = message.get('type', 'private')
        
        # Add to message history
        if msg_type == 'private':
            self.messaging.add_private_message(sender_ip, sender_name, content)
        else:
            self.messaging.add_group_message(sender_ip, sender_name, content)
        
        # Add to incoming messages for display
        formatted_msg = self.messaging.format_message(message)
        with self.message_lock:
            self.incoming_messages.append(formatted_msg)
        
        # Play notification sound
        self.sound.play_notification("message")
    
    def message_display_thread(self):
        """Thread to handle message notifications."""
        while self.running:
            time.sleep(0.1)  # Check every 100ms

def main():
    """Main entry point."""
    try:
        app = BhilNet()
        app.start()
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        logger.error(f"Application error: {e}")
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
