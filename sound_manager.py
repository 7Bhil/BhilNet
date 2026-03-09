"""Sound notification manager for BhilNet."""

import platform
import threading
import time
from typing import Optional

class SoundManager:
    """Handles sound notifications across platforms."""
    
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.system = platform.system()
        self._last_sound_time = 0
        self._sound_cooldown = 0.5  # Prevent sound spam
    
    def enable(self):
        """Enable sound notifications."""
        self.enabled = True
    
    def disable(self):
        """Disable sound notifications."""
        self.enabled = False
    
    def play_notification(self, sound_type: str = "message"):
        """Play a notification sound."""
        if not self.enabled:
            return
        
        # Prevent sound spam
        current_time = time.time()
        if current_time - self._last_sound_time < self._sound_cooldown:
            return
        
        self._last_sound_time = current_time
        
        # Play sound in separate thread to avoid blocking
        threading.Thread(target=self._play_sound, args=(sound_type,), daemon=True).start()
    
    def _play_sound(self, sound_type: str):
        """Play sound based on platform and type."""
        try:
            if self.system == "Windows":
                self._play_windows_sound(sound_type)
            elif self.system == "Darwin":  # macOS
                self._play_macos_sound(sound_type)
            else:  # Linux and others
                self._play_linux_sound(sound_type)
        except Exception:
            # Silently fail if sound doesn't work
            pass
    
    def _play_windows_sound(self, sound_type: str):
        """Play sound on Windows."""
        try:
            import winsound
            
            if sound_type == "message":
                winsound.MessageBeep(winsound.MB_ICONINFORMATION)
            elif sound_type == "user_join":
                winsound.MessageBeep(winsound.MB_OK)
            elif sound_type == "user_leave":
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            else:
                winsound.Beep(800, 200)  # Custom beep
        except ImportError:
            # Fallback if winsound not available
            pass
    
    def _play_macos_sound(self, sound_type: str):
        """Play sound on macOS."""
        try:
            import os
            
            if sound_type == "message":
                os.system("afplay /System/Library/Sounds/Glass.aiff")
            elif sound_type == "user_join":
                os.system("afplay /System/Library/Sounds/Ping.aiff")
            elif sound_type == "user_leave":
                os.system("afplay /System/Library/Sounds/Sosumi.aiff")
            else:
                # Try to play a default sound
                os.system("afplay /System/Library/Sounds/Ping.aiff")
        except:
            pass
    
    def _play_linux_sound(self, sound_type: str):
        """Play sound on Linux."""
        try:
            import os
            
            # Try different sound players
            sound_commands = [
                "paplay",  # PulseAudio (most common)
                "aplay",   # ALSA
                "mplayer", # MPlayer
                "ffplay"   # FFmpeg
            ]
            
            sound_files = {
                "message": "/usr/share/sounds/alsa/Front_Left.wav",
                "user_join": "/usr/share/sounds/alsa/Front_Right.wav",
                "user_leave": "/usr/share/sounds/alsa/Rear_Left.wav"
            }
            
            sound_file = sound_files.get(sound_type, sound_files["message"])
            
            for cmd in sound_commands:
                if self._command_exists(cmd):
                    if cmd == "ffplay":
                        os.system(f"{cmd} -nodisp -autoexit {sound_file} 2>/dev/null")
                    else:
                        os.system(f"{cmd} {sound_file} 2>/dev/null")
                    break
            
            # Fallback to system beep
            os.system("echo -e '\a' 2>/dev/null")
            
        except:
            pass
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists on the system."""
        try:
            import subprocess
            subprocess.run(["which", command], capture_output=True, check=True)
            return True
        except:
            return False
    
    def test_sound(self, sound_type: str = "message"):
        """Test a sound notification."""
        print(f"Playing {sound_type} sound...")
        self.play_notification(sound_type)
        time.sleep(1)
        print("Test complete.")
