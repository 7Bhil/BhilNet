# Quick Start Guide - New Features

## 🎉 New Features Added!

### 1. Configuration Persistence
Your username and settings are now saved automatically!

- Username is remembered between sessions
- Settings stored in `bhilnet_config.json`
- Auto-load on startup

### 2. Quick Messages (Shortcuts)
Use these shortcuts for fast messaging:

- `:hi` → "Hello everyone!"
- `:bye` → "Goodbye!"  
- `:brb` → "Be right back"
- `:coffee` → "Going for coffee ☕"

### 3. User Status
Set your availability status:

- 🟢 **Online** - Available and active
- 🟡 **Away** - Away from keyboard (auto after 5 min)
- 🔴 **Busy** - Do not disturb
- ⚫ **Invisible** - Hidden from others

### 4. Sound Notifications
Get audio alerts for:

- New messages received
- Users joining/leaving
- Configurable on/off

## 🚀 How to Use

### First Run
```bash
python main.py
```
1. Choose your username (saved automatically)
2. See the enhanced interface with status
3. Try the quick message shortcuts!

### Quick Messages
Instead of typing long messages, just type:
```
:hi
:bye
:brb
```

### Status Management
- **Auto-away**: Automatically sets to "away" after 5 minutes of inactivity
- **Manual status**: Change status from the menu
- **Activity tracking**: Any interaction resets auto-away timer

### Sound Settings
- Toggle sounds on/off from the menu
- Different sounds for different events
- Cross-platform support (Windows/Linux/macOS)

## 📋 Enhanced Menu

The menu now includes:
```
1 - Send private message
2 - Send group message  
3 - Refresh users
4 - Change status
5 - Toggle sound
6 - View message history
7 - Settings
8 - Quit
```

## 🔧 Configuration File

Your settings are saved in `bhilnet_config.json`:

```json
{
  "username": "your_name",
  "encryption_enabled": true,
  "notification_sound": true,
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
```

## 🎯 Tips & Tricks

### Productivity
1. Use quick messages for common responses
2. Set status to "Busy" when working
3. Enable sounds for important notifications

### Privacy  
1. Use "Invisible" status to appear offline
2. Disable sounds for silent operation
3. Clear message history regularly

### Customization
1. Edit `bhilnet_config.json` for custom shortcuts
2. Modify auto-away timeout in settings
3. Choose your preferred theme

## 🔍 What's Next?

Coming soon:
- File transfer between users
- Message search functionality  
- Custom themes and colors
- Voice chat capabilities

## 🐛 Troubleshooting

**Sounds not working?**
- Check system volume
- Verify audio permissions
- Try the sound test in settings

**Status not updating?**
- Check auto-away is enabled
- Update activity by interacting with app
- Restart if issues persist

**Configuration not saving?**
- Check file permissions
- Ensure disk space available
- Delete corrupted config file to reset
