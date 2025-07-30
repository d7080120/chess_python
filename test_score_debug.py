#!/usr/bin/env python3
"""
Test script to debug move numbering system
"""
import sys
sys.path.append('It1_interfaces')

from ScoreManager import ScoreManager

def test_move_numbering():
    """Test the move numbering system"""
    # צור mock game object
    class MockGame:
        pass
    
    mock_game = MockGame()
    score_manager = ScoreManager(mock_game)
    
    # הוסף כמה מהלכים לשחקן 1
    print("=== Adding moves for Player 1 ===")
    for i in range(15):
        from_pos = (i % 8, 6)  # חלשא כליs בשולה הfooter 
        to_pos = (i % 8, 5)    # זח forwards ב-1
        piece_id = f"PW{i%8}"   # כלי לבן
        score_manager.record_move(piece_id, from_pos, to_pos)
        print(f"Added move {i+1}: {piece_id} from {from_pos} to {to_pos}")
    
    print("\n=== Testing get_player1_recent_moves_with_numbers(10) ===")
    recent_moves = score_manager.get_player1_recent_moves_with_numbers(10)
    for move_number, move in recent_moves:
        print(f"Move {move_number}: {move}")
    
    print(f"\nTotal player1_moves: {len(score_manager.player1_moves)}")
    print(f"All moves: {score_manager.player1_moves}")
    
    # נסה עם שחקן 2
    print("\n=== Adding moves for Player 2 ===")
    for i in range(12):
        from_pos = (i % 8, 1)  # כלים שחורים בשורה העליונה
        to_pos = (i % 8, 2)    # זחו קדמה ב-1
        piece_id = f"PB{i%8}"   # כלי שחור
        score_manager.record_move(piece_id, from_pos, to_pos)
        print(f"Added move {i+1}: {piece_id} from {from_pos} to {to_pos}")
    
    print("\n=== Testing get_player2_recent_moves_with_numbers(10) ===")
    recent_moves = score_manager.get_player2_recent_moves_with_numbers(10)
    for move_number, move in recent_moves:
        print(f"Move {move_number}: {move}")

if __name__ == "__main__":
    test_move_numbering()
