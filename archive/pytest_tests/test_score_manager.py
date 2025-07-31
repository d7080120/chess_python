"""
test_score_manager.py - בדיקות ל-ScoreManager עם pytest
"""
import pytest
from unittest.mock import Mock
from ScoreManager import ScoreManager, MoveRecord


class TestMoveRecord:
    """בדיקות ל-MoveRecord"""
    
    def test_move_record_creation(self):
        """בדיקת יצירת MoveRecord"""
        move = MoveRecord("PW", (0, 6), (0, 5), "move")
        
        assert move.piece_id == "PW"
        assert move.from_pos == (0, 6)
        assert move.to_pos == (0, 5)
        assert move.move_type == "move"
        assert move.captured_piece is None
        assert move.timestamp is not None
    
    def test_move_record_capture(self):
        """בדיקת MoveRecord עם תפיסה"""
        move = MoveRecord("NW", (1, 7), (2, 5), "capture", "PB")
        
        assert move.piece_id == "NW"
        assert move.move_type == "capture"
        assert move.captured_piece == "PB"
    
    def test_move_record_string_representation(self):
        """בדיקת ייצוג המחרוזת של MoveRecord"""
        # מהלך רגיל
        move = MoveRecord("PW", (0, 6), (0, 5), "move")
        assert str(move) == "PW: A2-A3"
        
        # תפיסה
        capture = MoveRecord("NW", (1, 7), (2, 5), "capture", "PB")
        assert str(capture) == "NW: B1xC3"


class TestScoreManager:
    """בדיקות ל-ScoreManager"""
    
    def test_score_manager_initialization(self, mock_game):
        """בדיקת אתחול ScoreManager"""
        sm = ScoreManager(mock_game)
        
        assert sm.game == mock_game
        assert sm.player1_score == 0
        assert sm.player2_score == 0
        assert len(sm.player1_moves) == 0
        assert len(sm.player2_moves) == 0
        assert "P" in sm.piece_values
        assert sm.piece_values["P"] == 1
        assert sm.piece_values["Q"] == 9
    
    def test_record_move_white_piece(self, score_manager):
        """בדיקת רישום מהלך של כלי לבן"""
        score_manager.record_move("PW", (0, 6), (0, 5), "move")
        
        assert len(score_manager.player1_moves) == 1
        assert len(score_manager.player2_moves) == 0
        
        move = score_manager.player1_moves[0]
        assert move.piece_id == "PW"
        assert move.from_pos == (0, 6)
        assert move.to_pos == (0, 5)
    
    def test_record_move_black_piece(self, score_manager):
        """בדיקת רישום מהלך של כלי שחור"""
        score_manager.record_move("PB", (0, 1), (0, 2), "move")
        
        assert len(score_manager.player1_moves) == 0
        assert len(score_manager.player2_moves) == 1
        
        move = score_manager.player2_moves[0]
        assert move.piece_id == "PB"
    
    def test_record_capture_white_captures_black(self, score_manager):
        """בדיקת רישום תפיסה - לבן תופס שחור"""
        initial_score = score_manager.player1_score
        
        score_manager.record_move("NW", (1, 7), (2, 5), "capture", "PB")
        
        # בדוק שהמהלך נרשם
        assert len(score_manager.player1_moves) == 1
        move = score_manager.player1_moves[0]
        assert move.move_type == "capture"
        assert move.captured_piece == "PB"
        
        # בדוק שהניקוד עודכן (רגלי = 1 נקודה)
        assert score_manager.player1_score == initial_score + 1
    
    def test_record_capture_black_captures_white(self, score_manager):
        """בדיקת רישום תפיסה - שחור תופס לבן"""
        initial_score = score_manager.player2_score
        
        score_manager.record_move("QB", (3, 0), (3, 6), "capture", "PW")
        
        # בדוק שהמהלך נרשם
        assert len(score_manager.player2_moves) == 1
        
        # בדוק שהניקוד עודכן (רגלי = 1 נקודה)
        assert score_manager.player2_score == initial_score + 1
    
    def test_piece_values_scoring(self, score_manager):
        """בדיקת ניקוד לפי סוגי כלים שונים"""
        # תפיסת רגלי (1 נקודה)
        score_manager.record_move("NW", (1, 7), (2, 5), "capture", "PB")
        assert score_manager.player1_score == 1
        
        # תפיסת סוס (3 נקודות)
        score_manager.record_move("NW", (2, 5), (3, 3), "capture", "NB")
        assert score_manager.player1_score == 4  # 1 + 3
        
        # תפיסת מלכה (9 נקודות)
        score_manager.record_move("NW", (3, 3), (4, 1), "capture", "QB")
        assert score_manager.player1_score == 13  # 1 + 3 + 9
    
    def test_get_recent_moves(self, score_manager):
        """בדיקת קבלת מהלכים אחרונים"""
        # הוסף כמה מהלכים
        moves = [
            ("PW", (0, 6), (0, 5), "move"),
            ("PW", (1, 6), (1, 4), "move"),
            ("PW", (2, 6), (2, 5), "move"),
        ]
        
        for piece_id, from_pos, to_pos, move_type in moves:
            score_manager.record_move(piece_id, from_pos, to_pos, move_type)
        
        recent = score_manager.get_player1_recent_moves(2)
        assert len(recent) == 2
        # בדוק שהמהלכים מסודרים מהחדש לישן
        assert "C2-C3" in recent[0]  # המהלך האחרון
        assert "B2-B4" in recent[1]  # המהלך לפני האחרון
    
    def test_move_history_limit(self, score_manager):
        """בדיקת הגבלת מספר המהלכים (10 מהלכים)"""
        # הוסף 15 מהלכים
        for i in range(15):
            score_manager.record_move("PW", (0, 6), (0, 5), "move")
        
        # בדוק שנשמרו רק 10
        assert len(score_manager.player1_moves) == 10
    
    def test_get_scores(self, score_manager):
        """בדיקת קבלת הניקוד"""
        score_manager.player1_score = 5
        score_manager.player2_score = 3
        
        scores = score_manager.get_scores()
        assert scores == (5, 3)
    
    def test_reset_scores(self, score_manager):
        """בדיקת איפוס הניקוד"""
        # הוסף מהלכים וניקוד
        score_manager.record_move("PW", (0, 6), (0, 5), "capture", "PB")
        score_manager.record_move("QB", (3, 0), (3, 6), "capture", "PW")
        
        assert score_manager.player1_score > 0
        assert score_manager.player2_score > 0
        assert len(score_manager.player1_moves) > 0
        assert len(score_manager.player2_moves) > 0
        
        # איפוס
        score_manager.reset_scores()
        
        assert score_manager.player1_score == 0
        assert score_manager.player2_score == 0
        assert len(score_manager.player1_moves) == 0
        assert len(score_manager.player2_moves) == 0
