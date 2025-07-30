"""
test_observer_system.py - בדיקות למערכת Observer עם pytest
"""
import pytest
from unittest.mock import Mock
from Command import Command
from ScoreManager import ScoreManager
from integration_setup import setup_observers
import time


class TestObserverIntegration:
    """בדיקות למערכת Observer המשולבת"""
    
    def test_observer_setup(self, mock_game):
        """בדיקת הגדרת observers"""
        subject, logger, scorer, sound_player, score_manager = setup_observers(mock_game)
        
        assert subject is not None
        assert logger is not None
        assert scorer is not None
        assert sound_player is not None
        assert score_manager is not None
        assert isinstance(score_manager, ScoreManager)
    
    def test_score_manager_receives_move_commands(self, observer_setup):
        """בדיקת קבלת פקודות move על ידי ScoreManager"""
        subject, logger, scorer, sound_player, score_manager = observer_setup
        
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
        
        # שליחת הפקודה
        subject.notify(move_cmd)
        
        # בדיקה שהמהלך נרשם
        assert len(score_manager.player1_moves) == 1
        move = score_manager.player1_moves[0]
        assert move.piece_id == "PW"
        assert move.move_type == "move"
    
    def test_score_manager_receives_capture_commands(self, observer_setup):
        """בדיקת קבלת פקודות תפיסה על ידי ScoreManager"""
        subject, logger, scorer, sound_player, score_manager = observer_setup
        
        # יצירת פקודת תפיסה (move עם captured_piece)
        capture_cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="NW",
            type="move",
            from_pos=(2, 7),
            to_pos=(1, 1),
            captured_piece="PB",
            target=(1, 1)
        )
        
        # שליחת הפקודה
        subject.notify(capture_cmd)
        
        # בדיקה שהתפיסה נרשמה
        assert len(score_manager.player1_moves) == 1
        move = score_manager.player1_moves[0]
        assert move.piece_id == "NW"
        assert move.move_type == "capture"
        assert move.captured_piece == "PB"
        
        # בדיקה שהניקוד עודכן
        assert score_manager.player1_score == 1  # רגלי = 1 נקודה
    
    def test_multiple_observers_receive_notifications(self, observer_setup):
        """בדיקה שכל ה-observers מקבלים הודעות"""
        subject, logger, scorer, sound_player, score_manager = observer_setup
        
        # יצירת פקודה
        move_cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="PW",
            type="move",
            from_pos=(0, 6),
            to_pos=(0, 5),
            captured_piece=None,
            target=(0, 5)
        )
        
        # שליחת הפקודה
        subject.notify(move_cmd)
        
        # בדיקה ש-ScoreManager קיבל
        assert len(score_manager.player1_moves) == 1
        
        # בדיקה ש-Logger קיבל (אם יש לו logs)
        if hasattr(logger, 'logs'):
            assert len(logger.logs) > 0
    
    def test_command_without_position_data(self, observer_setup):
        """בדיקת טיפול בפקודה ללא מידע מיקום"""
        subject, logger, scorer, sound_player, score_manager = observer_setup
        
        # יצירת פקודה ללא מידע מיקום
        incomplete_cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="PW",
            type="move",
            from_pos=None,
            to_pos=None,
            captured_piece=None,
            target=(0, 5)
        )
        
        # שליחת הפקודה
        subject.notify(incomplete_cmd)
        
        # בדיקה שלא נרשם מהלך
        assert len(score_manager.player1_moves) == 0
        assert len(score_manager.player2_moves) == 0
    
    def test_jump_commands_are_processed(self, observer_setup):
        """בדיקת עיבוד פקודות jump"""
        subject, logger, scorer, sound_player, score_manager = observer_setup
        
        # יצירת פקודת jump
        jump_cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="NW",
            type="jump",
            from_pos=(1, 7),
            to_pos=(2, 5),
            captured_piece=None,
            target=(2, 5)
        )
        
        # שליחת הפקודה
        subject.notify(jump_cmd)
        
        # בדיקה שהמהלך נרשם
        assert len(score_manager.player1_moves) == 1
        move = score_manager.player1_moves[0]
        assert move.piece_id == "NW"
        assert move.move_type == "move"  # jump נרשם כ-move


class TestScoreManagerObserver:
    """בדיקות ספציפיות ל-ScoreManager כ-Observer"""
    
    def test_update_method_with_move_command(self, score_manager, sample_command):
        """בדיקת מתודת update עם פקודת move"""
        score_manager.update(sample_command)
        
        assert len(score_manager.player1_moves) == 1
        move = score_manager.player1_moves[0]
        assert move.piece_id == sample_command.piece_id
        assert move.from_pos == sample_command.from_pos
        assert move.to_pos == sample_command.to_pos
    
    def test_update_method_with_capture_command(self, score_manager, capture_command):
        """בדיקת מתודת update עם פקודת תפיסה"""
        initial_score = score_manager.player1_score
        
        score_manager.update(capture_command)
        
        assert len(score_manager.player1_moves) == 1
        move = score_manager.player1_moves[0]
        assert move.move_type == "capture"
        assert move.captured_piece == "PB"
        
        # בדיקה שהניקוד עודכן
        assert score_manager.player1_score == initial_score + 1
    
    def test_update_ignores_non_move_commands(self, score_manager):
        """בדיקה שמתודת update מתעלמת מפקודות שאינן move/jump"""
        # יצירת פקודה מסוג אחר
        other_cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="PW",
            type="reset",
            from_pos=(0, 6),
            to_pos=(0, 5),
            captured_piece=None,
            target=(0, 5)
        )
        
        score_manager.update(other_cmd)
        
        # בדיקה שלא נרשם מהלך
        assert len(score_manager.player1_moves) == 0
        assert len(score_manager.player2_moves) == 0
