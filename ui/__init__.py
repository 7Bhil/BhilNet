"""Terminal UI module for BhilNet."""

import os
import sys
import time
import threading
from typing import Dict, List, Optional
import colorama
from colorama import Fore, Style, Back

colorama.init()

class TerminalUI:
    """Handles terminal interface for BhilNet."""
    
    def __init__(self):
        self.username = ""
        self.current_users = {}
        self.message_history = []
        self.lock = threading.Lock()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen."""
        import platform
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def get_username(self) -> str:
        """Get username from user input."""
        self.clear_screen()
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}    BhilNet - LAN Terminal Chat v1.0")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print()
        
        while True:
            username = input(f"{Fore.YELLOW}Choose your username: {Style.RESET_ALL}").strip()
            if username and len(username) >= 2 and len(username) <= 20:
                self.username = username
                return username
            print(f"{Fore.RED}Username must be 2-20 characters long!{Style.RESET_ALL}")
    
    def show_main_interface(self, users: Dict[str, Dict], recent_messages: List[str] = None):
        """Display the main interface."""
        self.clear_screen()
        
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}    BhilNet - LAN Terminal Chat v1.0")
        print(f"{Fore.CYAN}    Logged in as: {Fore.GREEN}{self.username}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print()
        
        # Show connected users
        print(f"{Fore.BLUE}Users connected:{Style.RESET_ALL}")
        if users:
            for i, (ip, user_info) in enumerate(users.items(), 1):
                print(f"  [{i}] {Fore.GREEN}{user_info['username']}{Style.RESET_ALL} - {ip}")
        else:
            print(f"  {Fore.YELLOW}No other users found on the network{Style.RESET_ALL}")
        
        print()
        
        # Show recent messages if provided
        if recent_messages:
            print(f"{Fore.MAGENTA}Recent messages:{Style.RESET_ALL}")
            for msg in recent_messages[-5:]:  # Show last 5 messages
                print(f"  {msg}")
            print()
        
        # Show menu
        print(f"{Fore.YELLOW}Menu:{Style.RESET_ALL}")
        print("  1 - Send private message")
        print("  2 - Send group message")
        print("  3 - Refresh users")
        print("  4 - View message history")
        print("  5 - Quit")
        print()
    
    def get_menu_choice(self) -> int:
        """Get user menu choice."""
        while True:
            try:
                choice = input(f"{Fore.CYAN}Enter your choice (1-5): {Style.RESET_ALL}").strip()
                if choice in ['1', '2', '3', '4', '5']:
                    return int(choice)
                print(f"{Fore.RED}Invalid choice! Please enter 1-5.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                return 5
    
    def select_user(self, users: Dict[str, Dict]) -> Optional[str]:
        """Let user select a recipient."""
        if not users:
            print(f"{Fore.YELLOW}No users available!{Style.RESET_ALL}")
            input("Press Enter to continue...")
            return None
        
        print(f"\n{Fore.BLUE}Select a user:{Style.RESET_ALL}")
        user_list = list(users.items())
        
        for i, (ip, user_info) in enumerate(user_list, 1):
            print(f"  [{i}] {Fore.GREEN}{user_info['username']}{Style.RESET_ALL} - {ip}")
        
        while True:
            try:
                choice = input(f"\n{Fore.CYAN}Enter user number (or 0 to cancel): {Style.RESET_ALL}").strip()
                if choice == '0':
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(user_list):
                    return user_list[choice_num - 1][0]
                
                print(f"{Fore.RED}Invalid choice! Please enter 0-{len(user_list)}.{Style.RESET_ALL}")
            except (ValueError, KeyboardInterrupt):
                return None
    
    def get_message(self, prompt: str = "Enter your message") -> Optional[str]:
        """Get message from user."""
        try:
            message = input(f"{Fore.CYAN}{prompt}: {Style.RESET_ALL}").strip()
            if message:
                return message
            return None
        except KeyboardInterrupt:
            return None
    
    def show_message_history(self, private_messages: Dict[str, List], group_messages: List):
        """Display message history."""
        self.clear_screen()
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}    Message History")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print()
        
        # Show group messages
        if group_messages:
            print(f"{Fore.MAGENTA}Group Messages:{Style.RESET_ALL}")
            for msg in group_messages[-10:]:  # Show last 10 messages
                print(f"  {msg}")
            print()
        
        # Show private messages
        if private_messages:
            print(f"{Fore.GREEN}Private Messages:{Style.RESET_ALL}")
            for user_ip, messages in private_messages.items():
                if messages:
                    print(f"  {Fore.BLUE}Conversation with {messages[0].get('sender_username', 'Unknown')}:{Style.RESET_ALL}")
                    for msg in messages[-5:]:  # Show last 5 messages per user
                        print(f"    {msg}")
                    print()
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    def show_notification(self, message: str, color: str = Fore.YELLOW):
        """Show a notification message."""
        print(f"\n{color}{message}{Style.RESET_ALL}")
        time.sleep(2)
    
    def display_incoming_message(self, message: str):
        """Display an incoming message without clearing the screen."""
        print(f"\n{Fore.MAGENTA}[NEW MESSAGE] {message}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def quit_screen(self):
        """Show quit screen."""
        self.clear_screen()
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}    Thank you for using BhilNet!")
        print(f"{Fore.CYAN}    Goodbye!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}")
