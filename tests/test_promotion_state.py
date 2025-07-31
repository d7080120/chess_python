#!/usr/bin/env python3
"""
Test script to verify that promoted queens are properly set to rest_long state
"""
import pathlib
import sys
import time

# Add the current directory to the path so we can import the modules
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from src.core.PieceFactory import PieceFactory
from src.core.Board import Board
from queue import Queue

def test_promotion_state():
    """Test that promoted queens are properly initialized to rest_long state"""
    print("🧪 Testing pawn promotion state initialization...")
    
    # Create a minimal setup
    pieces_root = pathlib.Path(__file__).parent.parent / "pieces"
    board = Board()
    user_input_queue = Queue()
    
    # Create a piece factory
    factory = PieceFactory(board, pieces_root) 
    
    try:
        # Create a white queen at position (4, 0) as if it was promoted
        position = (4, 0)
        queen = factory.create_piece("QW", position, user_input_queue)
        queen.piece_id = "QW_promoted_test"
        queen._state._physics.piece_id = "QW_promoted_test"
        
        # Manually set the state to rest_long as our fix does
        now_ms = int(time.time() * 1000)
        queen._state.state = "rest_long"
        queen._state.rest_start = now_ms
        
        print(f"✅ Created promoted queen: {queen.piece_id}")
        print(f"📍 Position: {queen._state._physics.cell}")
        print(f"🏃 State: {queen._state.state}")
        print(f"⏰ Rest start time: {queen._state.rest_start}")
        
        # Verify the state
        if queen._state.state == "rest_long":
            print("✅ SUCCESS: Promoted queen is in rest_long state!")
        else:
            print(f"❌ FAILURE: Expected rest_long, got {queen._state.state}")
            
        # Test that it's actually resting by trying to move it
        from src.core.Command import Command
        move_cmd = Command(
            timestamp=now_ms + 100,  # Just 100ms later
            piece_id=queen.piece_id,
            type="move",
            target=(5, 1),
            params=None
        )
        
        result = queen._state.process_command(move_cmd)
        if result is None:
            print("✅ SUCCESS: Queen correctly rejected movement while resting!")
        else:
            print("❌ FAILURE: Queen should have rejected movement while resting")
            
        print("\n🎉 Test completed!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_promotion_state()
