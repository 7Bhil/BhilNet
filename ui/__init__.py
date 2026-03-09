"""Interface terminal pour BhilNet.

Développé par Bhilal CHITOU (Bhil€)
"""

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
    
    def get_username(self, default: str = "") -> str:
        """Get username from user input."""
        self.clear_screen()
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}    BhilNet - Chat Terminal Réseau Local v1.0")
        print(f"{Fore.CYAN}    Développé par Bhilal CHITOU (Bhil€)")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print()
        
        if default:
            prompt = f"{Fore.YELLOW}Choisissez votre pseudo [{default}]: {Style.RESET_ALL}"
        else:
            prompt = f"{Fore.YELLOW}Choisissez votre pseudo: {Style.RESET_ALL}"
        
        while True:
            username = input(prompt).strip()
            if not username and default:
                username = default
            
            if username and len(username) >= 2 and len(username) <= 20:
                self.username = username
                return username
            print(f"{Fore.RED}Le pseudo doit contenir 2-20 caractères !{Style.RESET_ALL}")
    
    def show_main_interface(self, users: Dict[str, Dict], recent_messages: List[str] = None, current_status: Dict[str, str] = None):
        """Display the main interface."""
        self.clear_screen()
        
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}    BhilNet - Chat Terminal Réseau Local v1.0")
        print(f"{Fore.CYAN}    Connecté en tant que: {Fore.GREEN}{self.username}{Style.RESET_ALL}")
        
        # Show status if provided
        if current_status:
            from user_status import UserStatus, StatusManager
            status_obj = UserStatus(current_status.get('status', 'online'))
            status_color = StatusManager.get_status_color(status_obj)
            status_emoji = StatusManager.get_status_emoji(status_obj)
            status_msg = current_status.get('message', '')
            print(f"{Fore.CYAN}    Status: {status_color}{status_emoji} {status_obj.value.upper()}{Style.RESET_ALL} {status_msg}")
        
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print()
        
        # Show connected users
        print(f"{Fore.BLUE}Utilisateurs connectés:{Style.RESET_ALL}")
        if users:
            for i, (ip, user_info) in enumerate(users.items(), 1):
                print(f"  [{i}] {Fore.GREEN}{user_info['username']}{Style.RESET_ALL} - {ip}")
        else:
            print(f"  {Fore.YELLOW}Aucun autre utilisateur trouvé sur le réseau{Style.RESET_ALL}")
        
        print()
        
        # Show recent messages if provided
        if recent_messages:
            print(f"{Fore.MAGENTA}Messages récents:{Style.RESET_ALL}")
            for msg in recent_messages[-5:]:  # Show last 5 messages
                print(f"  {msg}")
            print()
        
        # Show menu
        print(f"{Fore.YELLOW}Menu:{Style.RESET_ALL}")
        print("  1 - Envoyer un message privé")
        print("  2 - Envoyer un message groupe")
        print("  3 - Actualiser les utilisateurs")
        print("  4 - Changer de statut")
        print("  5 - Activer/désactiver les sons")
        print("  6 - Voir l'historique des messages")
        print("  7 - Paramètres")
        print("  8 - Quitter")
        print()
    
    def get_menu_choice(self) -> int:
        """Get user menu choice."""
        while True:
            try:
                choice = input(f"{Fore.CYAN}Entrez votre choix (1-8): {Style.RESET_ALL}").strip()
                if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    return int(choice)
                print(f"{Fore.RED}Choix invalide ! Entrez 1-8.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                return 8
    
    def select_user(self, users: Dict[str, Dict]) -> Optional[str]:
        """Let user select a recipient."""
        if not users:
            print(f"{Fore.YELLOW}Aucun utilisateur disponible !{Style.RESET_ALL}")
            input("Appuyez sur Entrée pour continuer...")
            return None
        
        print(f"\n{Fore.BLUE}Sélectionnez un utilisateur:{Style.RESET_ALL}")
        user_list = list(users.items())
        
        for i, (ip, user_info) in enumerate(user_list, 1):
            print(f"  [{i}] {Fore.GREEN}{user_info['username']}{Style.RESET_ALL} - {ip}")
        
        while True:
            try:
                choice = input(f"\n{Fore.CYAN}Entrez le numéro d'utilisateur (ou 0 pour annuler): {Style.RESET_ALL}").strip()
                if choice == '0':
                    return None
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(user_list):
                    return user_list[choice_num - 1][0]
                
                print(f"{Fore.RED}Choix invalide ! Entrez 0-{len(user_list)}.{Style.RESET_ALL}")
            except (ValueError, KeyboardInterrupt):
                return None
    
    def get_message(self, prompt: str = "Entrez votre message") -> Optional[str]:
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
        print(f"{Fore.CYAN}    Historique des Messages")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
        print()
        
        # Show group messages
        if group_messages:
            print(f"{Fore.MAGENTA}Messages de groupe:{Style.RESET_ALL}")
            for msg in group_messages[-10:]:  # Show last 10 messages
                print(f"  {msg}")
            print()
        
        # Show private messages
        if private_messages:
            print(f"{Fore.GREEN}Messages privés:{Style.RESET_ALL}")
            for user_ip, messages in private_messages.items():
                if messages:
                    print(f"  {Fore.BLUE}Conversation avec {messages[0].get('sender_username', 'Inconnu')}:{Style.RESET_ALL}")
                    for msg in messages[-5:]:  # Show last 5 messages per user
                        print(f"    {msg}")
                    print()
        
        input(f"\n{Fore.YELLOW}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
    
    def show_notification(self, message: str, color: str = Fore.YELLOW):
        """Show a notification message."""
        print(f"\n{color}{message}{Style.RESET_ALL}")
        time.sleep(2)
    
    def display_incoming_message(self, message: str):
        """Display an incoming message without clearing the screen."""
        print(f"\n{Fore.MAGENTA}[NOUVEAU MESSAGE] {message}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")
    
    def quit_screen(self):
        """Show quit screen."""
        self.clear_screen()
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}    Merci d'utiliser BhilNet !")
        print(f"{Fore.CYAN}    Au revoir !{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.CYAN}    Développé par Bhilal CHITOU (Bhil€)")
        print(f"{Fore.CYAN}    Contact: 7bhilal.chitou7@gmail.com")
        print(f"{Fore.CYAN}{'='*50}")
