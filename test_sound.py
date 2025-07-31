#!/usr/bin/env python3
"""
בדיקה מהירה של מערכת הסאונד
"""

# נבדוק אם pygame עובד
try:
    import pygame
    print("✅ pygame מותקן")
    pygame.mixer.init()
    print("✅ pygame.mixer התאתחל")
except Exception as e:
    print(f"❌ בעיה ב-pygame: {e}")

# נבדוק אם SoundPlayer עובד
try:
    from src.ui.sound_player import SoundPlayer
    sound_player = SoundPlayer()
    print("✅ SoundPlayer נוצר בהצלחה")
except Exception as e:
    print(f"❌ בעיה ב-SoundPlayer: {e}")

# נבדוק אם יש קבצי סאונד
import pathlib
pieces_path = pathlib.Path("assets/pieces")
if pieces_path.exists():
    sound_files = list(pieces_path.glob("*/sounds/*.mp3"))
    print(f"✅ נמצאו {len(sound_files)} קבצי סאונד")
    if sound_files:
        test_sound = sound_files[0]
        print(f"🎵 בודק קובץ סאונד: {test_sound}")
        try:
            sound_player.play(str(test_sound))
            print("✅ ניגון הצליח (אם יש רמקולים)")
        except Exception as e:
            print(f"❌ בעיה בניגון: {e}")
else:
    print("❌ תיקיית assets/pieces לא קיימת")
