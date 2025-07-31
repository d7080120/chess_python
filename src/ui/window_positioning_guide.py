"""
🎮 Window Positioning Guide for Chess Game
==========================================

To change window positions in the game:

📝 Edit settings file:
1. Open the file: window_settings.py
2. Change the following values:

📍 Position options:
   "top-left" = Top-left corner (0, 0)
   "center"   = Screen center

🔧 Examples:

For top-left corner opening:
    PLAYER_DIALOG_POSITION = "top-left"
    GAME_WINDOW_POSITION = "top-left"

For center screen opening:
    PLAYER_DIALOG_POSITION = "center"
    GAME_WINDOW_POSITION = "center"

For combination (dialog in corner, game in center):
    PLAYER_DIALOG_POSITION = "top-left"
    GAME_WINDOW_POSITION = "center"

💡 Tips:
- "top-left" is good for small screens or when you want to see other windows
- "center" is good for large screens and game focus
- Changes take effect on next game launch

🚀 Run the game:
python main.py

📋 Current Settings:
Edit the window_settings.py file to customize window positions according to your preferences.
"""
