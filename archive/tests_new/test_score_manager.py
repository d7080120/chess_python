"""
test_score_manager.py - Tests for ScoreManager with Observer pattern
"""
import pytest
from unittest.mock import Mock
import time


class TestMoveRecord:
    """Tests for MoveRecord class"""
    
    def test_move_record_creation(self):
        """Test creating a MoveRecord"""
        from ScoreManager import MoveRecord
        
        move = MoveRecord("PW0", (0, 6), (0, 5), "move")
        
        assert move.piece_id == "PW0"
        assert move.from_pos == (0, 6)
        assert move.to_pos == (0, 5)
        assert move.move_type == "move"
        assert move.captured_piece is None
        assert isinstance(move.timestamp, float)
    
    def test_move_record_capture(self):
        """Test creating a capture MoveRecord"""
        from ScoreManager import MoveRecord
        
        move = MoveRecord("NB0", (1, 0), (2, 2), "capture", "PW1")
        
        assert move.piece_id == "NB0"
        assert move.from_pos == (1, 0)
        assert move.to_pos == (2, 2)
        assert move.move_type == "capture"
        assert move.captured_piece == "PW1"
    
    def test_move_record_string_regular(self):
        """Test string representation of regular move"""
        from ScoreManager import MoveRecord
        
        move = MoveRecord("PW0", (0, 6), (0, 5), "move")
        result = str(move)
        
        assert "PW0" in result
        assert "A2" in result  # (0, 6) -> A2
        assert "A3" in result  # (0, 5) -> A3
        assert "-" in result
        assert "x" not in result
    
    def test_move_record_string_capture(self):
        """Test string representation of capture move"""
        from ScoreManager import MoveRecord
        
        move = MoveRecord("NB0", (1, 0), (2, 2), "capture", "PW1")
        result = str(move)
        
        assert "NB0" in result
        assert "B8" in result  # (1, 0) -> B8
        assert "C6" in result  # (2, 2) -> C6
        assert "x" in result
        assert "-" not in result


class TestScoreManager:
    """Tests for ScoreManager class"""
    
    def test_score_manager_creation(self, mock_game):
        """Test creating ScoreManager"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        
        assert manager.game == mock_game
        assert manager.player1_score == 0
        assert manager.player2_score == 0
        assert len(manager.player1_moves) == 0
        assert len(manager.player2_moves) == 0
        assert manager.piece_values['P'] == 1
        assert manager.piece_values['Q'] == 9
    
    def test_record_move_white_player(self, mock_game):
        """Test recording move for white player"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        manager.record_move("PW0", (0, 6), (0, 5), "move")
        
        assert len(manager.player1_moves) == 1
        assert len(manager.player2_moves) == 0
        assert manager.player1_moves[0].piece_id == "PW0"
        assert manager.player1_moves[0].move_type == "move"
    
    def test_record_move_black_player(self, mock_game):
        """Test recording move for black player"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        manager.record_move("PB0", (0, 1), (0, 2), "move")
        
        assert len(manager.player1_moves) == 0
        assert len(manager.player2_moves) == 1
        assert manager.player2_moves[0].piece_id == "PB0"
        assert manager.player2_moves[0].move_type == "move"
    
    def test_record_capture_scoring(self, mock_game):
        """Test that captures update score correctly"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        
        # White captures black pawn
        manager.record_move("NW0", (1, 7), (2, 2), "capture", "PB0")
        
        assert manager.player1_score == 1  # Pawn value
        assert manager.player2_score == 0
        assert len(manager.player1_moves) == 1
        assert manager.player1_moves[0].move_type == "capture"
    
    def test_capture_different_pieces(self, mock_game):
        """Test capturing different piece types gives correct scores"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        
        # Test different piece values
        test_cases = [
            ("PB0", 1),  # Pawn
            ("NB0", 3),  # Knight
            ("BB0", 3),  # Bishop
            ("RB0", 5),  # Rook
            ("QB0", 9),  # Queen
        ]
        
        initial_score = 0
        for piece_id, expected_value in test_cases:
            manager.record_move("PW0", (0, 6), (1, 1), "capture", piece_id)
            initial_score += expected_value
            assert manager.player1_score == initial_score
    
    def test_observer_update_regular_move(self, mock_game, sample_command):
        """Test Observer update with regular move"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        manager.update(sample_command)
        
        assert len(manager.player1_moves) == 1
        assert manager.player1_moves[0].move_type == "move"
        assert manager.player1_score == 0  # No capture
    
    def test_observer_update_capture_move(self, mock_game, capture_command):
        """Test Observer update with capture move"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        manager.update(capture_command)
        
        assert len(manager.player2_moves) == 1
        assert manager.player2_moves[0].move_type == "capture"
        assert manager.player2_score == 1  # Captured pawn
    
    def test_move_history_limit(self, mock_game):
        """Test that move history is limited to 10 moves per player"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        
        # Add 15 moves for white player
        for i in range(15):
            manager.record_move(f"PW{i%8}", (i%8, 6), (i%8, 5), "move")
        
        assert len(manager.player1_moves) == 10  # Limited to 10
        assert manager.player1_moves[0].piece_id == "PW5"  # First 5 were removed
        assert manager.player1_moves[-1].piece_id == "PW6"  # Last one (14 % 8 = 6)
    
    def test_get_recent_moves_ordering(self, mock_game):
        """Test that recent moves are returned newest first"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        
        # Add some moves
        moves = ["PW0", "PW1", "PW2"]
        for piece_id in moves:
            manager.record_move(piece_id, (0, 6), (0, 5), "move")
        
        recent = manager.get_player1_recent_moves()
        
        assert len(recent) == 3
        assert "PW2" in recent[0]  # Newest first
        assert "PW1" in recent[1]
        assert "PW0" in recent[2]  # Oldest last
    
    def test_reset_scores(self, mock_game):
        """Test resetting scores and move history"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        
        # Add some data
        manager.record_move("PW0", (0, 6), (0, 5), "capture", "PB0")
        manager.record_move("PB1", (1, 1), (1, 2), "move")
        
        assert manager.player1_score > 0
        assert len(manager.player1_moves) > 0
        assert len(manager.player2_moves) > 0
        
        # Reset
        manager.reset_scores()
        
        assert manager.player1_score == 0
        assert manager.player2_score == 0
        assert len(manager.player1_moves) == 0
        assert len(manager.player2_moves) == 0
    
    def test_get_scores(self, mock_game):
        """Test getting current scores"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        
        # Initial scores
        scores = manager.get_scores()
        assert scores == (0, 0)
        
        # After white captures
        manager.record_move("PW0", (0, 6), (1, 1), "capture", "PB0")
        scores = manager.get_scores()
        assert scores == (1, 0)
        
        # After black captures
        manager.record_move("PB1", (1, 1), (0, 6), "capture", "PW1")
        scores = manager.get_scores()
        assert scores == (1, 1)
    
    def test_get_move_count(self, mock_game):
        """Test getting move counts"""
        from ScoreManager import ScoreManager
        
        manager = ScoreManager(mock_game)
        
        # Initial count
        counts = manager.get_move_count()
        assert counts == (0, 0)
        
        # After moves
        manager.record_move("PW0", (0, 6), (0, 5), "move")
        manager.record_move("PW1", (1, 6), (1, 5), "move")
        manager.record_move("PB0", (0, 1), (0, 2), "move")
        
        counts = manager.get_move_count()
        assert counts == (2, 1)  # (white_moves, black_moves)
