"""
test_observer_integration.py - Tests for Observer pattern integration
"""
import pytest
from unittest.mock import Mock
import time


class TestObserverIntegration:
    """Tests for Observer pattern integration with ScoreManager"""
    
    def test_setup_observers_creates_score_manager(self):
        """Test that setup_observers creates ScoreManager correctly"""
        from integration_setup import setup_observers
        
        mock_game = Mock()
        result = setup_observers(mock_game)
        
        assert len(result) == 5  # subject, logger, scorer, sound_player, score_manager
        subject, logger, scorer, sound_player, score_manager = result
        
        assert score_manager is not None
        assert score_manager.game == mock_game
        assert hasattr(score_manager, 'update')  # Is Observer
    
    def test_observer_receives_move_notifications(self):
        """Test that ScoreManager receives move notifications"""
        from integration_setup import setup_observers
        from Command import Command
        
        mock_game = Mock()
        subject, logger, scorer, sound_player, score_manager = setup_observers(mock_game)
        
        # Create move command
        cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="PW0",
            type="move",
            from_pos=(0, 6),
            to_pos=(0, 5),
            captured_piece=None,
            target=(0, 5)
        )
        
        # Notify observers
        subject.notify(cmd)
        
        # Check that ScoreManager recorded the move
        assert len(score_manager.player1_moves) == 1
        assert score_manager.player1_moves[0].piece_id == "PW0"
        assert score_manager.player1_moves[0].move_type == "move"
    
    def test_observer_receives_capture_notifications(self):
        """Test that ScoreManager receives capture notifications"""
        from integration_setup import setup_observers
        from Command import Command
        
        mock_game = Mock()
        subject, logger, scorer, sound_player, score_manager = setup_observers(mock_game)
        
        # Create capture command (move with captured_piece)
        cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="NB0",
            type="move",  # Capture is move with captured_piece
            from_pos=(1, 0),
            to_pos=(2, 2),
            captured_piece="PW1",
            target=(2, 2)
        )
        
        # Notify observers
        subject.notify(cmd)
        
        # Check that ScoreManager recorded the capture
        assert len(score_manager.player2_moves) == 1
        assert score_manager.player2_moves[0].piece_id == "NB0"
        assert score_manager.player2_moves[0].move_type == "capture"
        assert score_manager.player2_moves[0].captured_piece == "PW1"
        assert score_manager.player2_score == 1  # Captured pawn
    
    def test_multiple_observers_receive_notifications(self):
        """Test that multiple observers receive the same notification"""
        from integration_setup import setup_observers
        from Command import Command
        
        mock_game = Mock()
        subject, logger, scorer, sound_player, score_manager = setup_observers(mock_game)
        
        # Create move command
        cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="PW0",
            type="move",
            from_pos=(0, 6),
            to_pos=(0, 5),
            captured_piece=None,
            target=(0, 5)
        )
        
        # Notify observers
        subject.notify(cmd)
        
        # Check that both logger and score_manager received notification
        assert len(logger.logs) > 0  # Logger received notification
        assert len(score_manager.player1_moves) == 1  # ScoreManager received notification
    
    def test_score_manager_handles_jump_commands(self):
        """Test that ScoreManager handles jump commands"""
        from integration_setup import setup_observers
        from Command import Command
        
        mock_game = Mock()
        subject, logger, scorer, sound_player, score_manager = setup_observers(mock_game)
        
        # Create jump command
        cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="NW0",
            type="jump",
            from_pos=(1, 7),
            to_pos=(2, 5),
            captured_piece=None,
            target=(2, 5)
        )
        
        # Notify observers
        subject.notify(cmd)
        
        # Check that ScoreManager recorded the jump as move
        assert len(score_manager.player1_moves) == 1
        assert score_manager.player1_moves[0].piece_id == "NW0"
        assert score_manager.player1_moves[0].move_type == "move"
    
    def test_score_manager_ignores_other_commands(self):
        """Test that ScoreManager ignores non-move/jump commands"""
        from integration_setup import setup_observers
        from Command import Command
        
        mock_game = Mock()
        subject, logger, scorer, sound_player, score_manager = setup_observers(mock_game)
        
        # Create reset command
        cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="PW0",
            type="reset",
            from_pos=None,
            to_pos=None,
            captured_piece=None,
            target=None
        )
        
        # Notify observers
        subject.notify(cmd)
        
        # Check that ScoreManager didn't record anything
        assert len(score_manager.player1_moves) == 0
        assert len(score_manager.player2_moves) == 0
    
    def test_command_without_position_data(self):
        """Test handling commands without position data"""
        from integration_setup import setup_observers
        from Command import Command
        
        mock_game = Mock()
        subject, logger, scorer, sound_player, score_manager = setup_observers(mock_game)
        
        # Create command without position data
        cmd = Command(
            timestamp=int(time.time() * 1000),
            piece_id="PW0",
            type="move",
            from_pos=None,  # Missing
            to_pos=None,    # Missing
            captured_piece=None,
            target=(0, 5)
        )
        
        # Notify observers - should not crash
        subject.notify(cmd)
        
        # Check that nothing was recorded
        assert len(score_manager.player1_moves) == 0
