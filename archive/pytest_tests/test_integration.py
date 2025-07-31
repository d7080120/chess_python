"""
test_integration.py - בדיקות אינטגרציה למערכת השחמט
"""
import pytest
from unittest.mock import Mock, patch
import numpy as np


class TestGameIntegration:
    """בדיקות אינטגרציה למשחק המלא"""
    
    @pytest.fixture
    def basic_game_setup(self):
        """הגדרת משחק בסיסי לבדיקות"""
        from GameRefactored import GameRefactored
        from Board import Board
        from PieceFactory import PieceFactory
        from img import Img
        import pathlib
        
        # יצירת תמונה בסיסית
        img = Img()
        img.img = np.zeros((800, 800, 3), dtype=np.uint8)
        img.img[:] = (100, 100, 100)  # רקע אפור
        
        # יצירת לוח
        board = Board(
            cell_W_pix=100, cell_H_pix=100,
            cell_H_m=1, cell_W_m=1,
            W_cells=8, H_cells=8,
            img=img
        )
        
        # יצירת factory
        pieces_root = pathlib.Path(__file__).parent.parent / "pieces"
        factory = PieceFactory(board, pieces_root)
        
        return board, factory
    
    def test_game_creation_with_observer_system(self, basic_game_setup):
        """בדיקת יצירת משחק עם מערכת Observer"""
        board, factory = basic_game_setup
        
        # יצירת כמה כלים
        pieces = [
            factory.create_piece("PW", (0, 6)),   # רגלי לבן
            factory.create_piece("PB", (1, 1)),   # רגלי שחור
        ]
        
        from GameRefactored import GameRefactored
        game = GameRefactored(pieces, board)
        
        # בדיקות בסיסיות
        assert game is not None
        assert hasattr(game, 'score_manager')
        assert hasattr(game, 'command_subject')
        assert len(game.pieces) == 2
    
    def test_move_recording_through_observer(self, basic_game_setup):
        """בדיקת רישום מהלכים דרך Observer"""
        board, factory = basic_game_setup
        
        pieces = [
            factory.create_piece("PW", (0, 6)),
            factory.create_piece("NW", (2, 7)),
        ]
        
        from GameRefactored import GameRefactored
        from Command import Command
        import time
        
        game = GameRefactored(pieces, board)
        
        # יצירת פקודת move
        move_cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="PW",
            type="move",
            from_pos=(0, 6),
            to_pos=(0, 5),
            captured_piece=None,
            target=(0, 5)
        )
        
        # שליחת הפקודה דרך subject
        game.command_subject.notify(move_cmd)
        
        # בדיקה שהמהלך נרשם
        assert len(game.score_manager.player1_moves) == 1
        move = game.score_manager.player1_moves[0]
        assert move.piece_id == "PW"
    
    def test_capture_scoring_integration(self, basic_game_setup):
        """בדיקת אינטגרציה של ניקוד תפיסות"""
        board, factory = basic_game_setup
        
        pieces = [
            factory.create_piece("NW", (2, 7)),   # סוס לבן
            factory.create_piece("PB", (1, 1)),   # רגלי שחור
        ]
        
        from GameRefactored import GameRefactored
        from Command import Command
        import time
        
        game = GameRefactored(pieces, board)
        
        # תפיסה
        capture_cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="NW",
            type="move",
            from_pos=(2, 7),
            to_pos=(1, 1),
            captured_piece="PB",
            target=(1, 1)
        )
        
        initial_score = game.score_manager.player1_score
        game.command_subject.notify(capture_cmd)
        
        # בדיקות
        assert len(game.score_manager.player1_moves) == 1
        assert game.score_manager.player1_score == initial_score + 1  # רגלי = 1 נקודה
        
        move = game.score_manager.player1_moves[0]
        assert move.move_type == "capture"
        assert move.captured_piece == "PB"


class TestMoveValidatorIntegration:
    """בדיקות אינטגרציה ל-MoveValidator"""
    
    def test_move_validator_creates_correct_commands(self):
        """בדיקה ש-MoveValidator יוצר פקודות נכונות"""
        # זה יהיה טסט מורכב יותר שיבדוק את MoveValidator
        # בינתיים נשאיר placeholder
        pass


class TestDrawManagerIntegration:
    """בדיקות אינטגרציה ל-DrawManager"""
    
    def test_draw_manager_displays_scores_and_moves(self):
        """בדיקה ש-DrawManager מציג ניקוד ומהלכים"""
        # טסט לעתיד - יבדוק שה-DrawManager משתמש ב-ScoreManager נכון
        pass
