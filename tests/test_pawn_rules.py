#!/usr/bin/env python3
"""Test pawn movement rules"""

import pathlib
from src.core.Board import Board
from src.core.GameRefactored import GameRefactored
from src.core.PieceFactory import PieceFactory
from src.graphics.img import Img

def test_pawn_rules():
    print("Testing pawn movement rules...")
    
    # Create board and factory
    img = Img()
    img_path = pathlib.Path(__file__).parent.parent / "board.png"
    img.read(str(img_path), size=(800, 800))
    
    board = Board(
        cell_W_pix=100, cell_H_pix=100, cell_H_m=1, cell_W_m=1,
        W_cells=8, H_cells=8, img=img
    )
    pieces_root = pathlib.Path(__file__).parent.parent / "pieces"
    factory = PieceFactory(board, pieces_root)
    
    # Create test pieces
    pieces = []
    
    # White pawn at starting position (4,6)
    white_start = factory.create_piece("PW", (4, 6), None)
    white_start.piece_id = "PW_start"
    white_start._state._physics.piece_id = "PW_start"
    pieces.append(white_start)
    
    # White pawn not at starting position (3, 4)
    white_middle = factory.create_piece("PW", (3, 4), None)
    white_middle.piece_id = "PW_middle"
    white_middle._state._physics.piece_id = "PW_middle"
    pieces.append(white_middle)
    
    # Black pawn for capture test (4, 3)
    black_target = factory.create_piece("PB", (4, 3), None)
    black_target.piece_id = "PB_target"
    black_target._state._physics.piece_id = "PB_target"
    pieces.append(black_target)
    
    # Create game
    game = GameRefactored(pieces, board)
    
    # Update pieces with game queues
    for piece in pieces:
        piece._state._physics.user_input_queue = game.user_input_queue
        piece._state._game_queue = game.game_queue
    
    print(f"White pawn start: {white_start._state._physics.cell}")
    print(f"White pawn middle: {white_middle._state._physics.cell}")
    print(f"Black pawn target: {black_target._state._physics.cell}")
    
    # Test cases: (piece, target_x, target_y, should_succeed, test_name)
    tests = [
        # Starting position pawn tests
        (white_start, 4, 5, True, "White start pawn - 1 step forward"),
        (white_start, 4, 4, True, "White start pawn - 2 steps forward"),
        
        # Non-starting position pawn tests
        (white_middle, 3, 3, True, "White middle pawn - 1 step forward"),
        (white_middle, 3, 2, False, "White middle pawn - 2 steps forward (invalid)"),
        (white_middle, 4, 3, True, "White middle pawn - diagonal capture"),
        (white_middle, 2, 3, False, "White middle pawn - diagonal no capture"),
        
        # Invalid moves
        (white_start, 5, 6, False, "White pawn - sideways"),
        (white_start, 4, 7, False, "White pawn - backwards"),
    ]
    
    results = []
    for i, (piece, target_x, target_y, should_succeed, test_name) in enumerate(tests, 1):
        print(f"\n{i}. {test_name}")
        print(f"   Trying: {piece.piece_id} from {piece._state._physics.cell} to ({target_x}, {target_y})")
        
        player_num = 1 if 'W' in piece.piece_id else 2
        move_result = game.move_validator._is_valid_move(piece, target_x, target_y, player_num)
        
        if move_result == should_succeed:
            print(f"   OK: {'Success' if move_result else 'Failed'}")
            results.append(True)
        else:
            print(f"   ERROR: Expected {'success' if should_succeed else 'failure'}, got {'success' if move_result else 'failure'}")
            results.append(False)
    
    # Summary
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\nResults: {success_count}/{total_count} tests passed")
    
    if success_count == total_count:
        print("SUCCESS: All pawn movement rules working correctly!")
        return True
    else:
        print("FAILURE: Some tests failed.")
        return False

if __name__ == "__main__":
    test_pawn_rules()
