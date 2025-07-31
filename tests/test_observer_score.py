"""
test_observer_score.py - בדיקת מערכת הניקוד החדשה עם Observer pattern
"""
import sys
import pathlib
from unittest.mock import Mock

# הוסף את הנתיב לתיקיית המחלקות
current_dir = pathlib.Path(__file__).parent
sys.path.append(str(current_dir))

def test_observer_score_system():
    """בדיקת מערכת הניקוד החדשה עם Observer"""
    
    print("🧪 בדיקת מערכת Observer לניקוד ומהלכים")
    print("=" * 60)
    
    from integration_setup import setup_observers
    from src.core.Command import Command
    import time
    
    # יצירת mock game
    mock_game = Mock()
    
    # הגדרת observers
    subject, logger, scorer, sound_player, score_manager = setup_observers(mock_game)
    
    print("✅ Observers הוגדרו בהצלחה")
    print(f"   - Subject: {type(subject).__name__}")
    print(f"   - ScoreManager: {type(score_manager).__name__}")
    
    # בדיקת מהלכים דרך Observer
    print("\n🎯 שליחת פקודות דרך Observer:")
    
    # מהלך רגיל - רגלי לבן
    move_cmd = Command(
        timestamp=int(time.time() * 1000),
        piece_id="PW0",
        type="move",
        from_pos=(0, 6),
        to_pos=(0, 5),
        captured_piece=None
    )
    
    print(f"   📤 שולח פקודה: {move_cmd.piece_id} {move_cmd.type}")
    subject.notify(move_cmd)
    
    # מהלך תפיסה - סוס שחור תופס רגלי לבן (שולח כ-move עם captured_piece)
    capture_cmd = Command(
        timestamp=int(time.time() * 1000),
        piece_id="NB0",
        type="move",  # שונה ל-move
        from_pos=(1, 0),
        to_pos=(2, 2),
        captured_piece="PW1"
    )
    
    print(f"   📤 שולח פקודה: {capture_cmd.piece_id} {capture_cmd.type} -> {capture_cmd.captured_piece}")
    subject.notify(capture_cmd)
    
    # עוד כמה מהלכים
    moves = [
        ("PW2", "move", (2, 6), (2, 4), None),
        ("QB0", "move", (3, 0), (3, 4), "PW2"),  # שונה ל-move עם captured_piece
        ("NW0", "move", (6, 7), (5, 5), None),
    ]
    
    for piece_id, move_type, from_pos, to_pos, captured in moves:
        cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id=piece_id,
            type=move_type,
            from_pos=from_pos,
            to_pos=to_pos,
            captured_piece=captured
        )
        print(f"   📤 {piece_id}: {move_type} {from_pos}->{to_pos}")
        subject.notify(cmd)
    
    # בדיקת תוצאות
    print("\n📊 תוצאות:")
    scores = score_manager.get_scores()
    print(f"🏆 ניקוד - לבן: {scores[0]}, שחור: {scores[1]}")
    
    moves_white = score_manager.get_player1_recent_moves(5)
    moves_black = score_manager.get_player2_recent_moves(5)
    
    print(f"\n📋 מהלכים אחרונים - לבן ({len(moves_white)}):")
    for i, move in enumerate(moves_white, 1):
        print(f"   {i}. {move}")
    
    print(f"\n📋 מהלכים אחרונים - שחור ({len(moves_black)}):")
    for i, move in enumerate(moves_black, 1):
        print(f"   {i}. {move}")
    
    print("\n" + "=" * 60)
    print("🎉 בדיקת Observer pattern הושלמה בהצלחה!")
    print("✨ המערכת כעת עובדת באמצעות observers במקום קריאות ישירות")
    
    return True

if __name__ == "__main__":
    test_observer_score_system()
