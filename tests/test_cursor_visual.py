#!/usr/bin/env python3
"""
Test to visualize how the cursors look when overlapping
"""
import cv2
import numpy as np

def test_cursor_visualization():
    """Test how the cursors look when they overlap"""
    print("🎨 Testing cursor visualization...")
    
    # Create a test board image (8x8 chess board)
    board_size = 400  # 400x400 pixels
    cell_size = board_size // 8  # 50x50 per cell
    
    # Create checkerboard pattern
    board = np.zeros((board_size, board_size, 3), dtype=np.uint8)
    for row in range(8):
        for col in range(8):
            color = (200, 200, 200) if (row + col) % 2 == 0 else (100, 100, 100)
            top_left = (col * cell_size, row * cell_size)
            bottom_right = ((col + 1) * cell_size - 1, (row + 1) * cell_size - 1)
            cv2.rectangle(board, top_left, bottom_right, color, -1)
    
    # Test case 1: Cursors at different positions
    board1 = board.copy()
    
    # Player 1 cursor at (2, 3) - Blue outer frame
    x1, y1 = 2, 3
    top_left_1 = (x1 * cell_size, y1 * cell_size)
    bottom_right_1 = ((x1 + 1) * cell_size - 1, (y1 + 1) * cell_size - 1)
    cv2.rectangle(board1, top_left_1, bottom_right_1, (255, 0, 0), 8)  # Blue thick
    
    # Player 2 cursor at (4, 5) - Red outer frame  
    x2, y2 = 4, 5
    top_left_2 = (x2 * cell_size, y2 * cell_size)
    bottom_right_2 = ((x2 + 1) * cell_size - 1, (y2 + 1) * cell_size - 1)
    cv2.rectangle(board1, top_left_2, bottom_right_2, (0, 0, 255), 8)  # Red thick
    
    print("✅ Created board with cursors at different positions")
    
    # Test case 2: Cursors at same position (the problem case)
    board2 = board.copy()
    
    # Both cursors at (3, 3) - OLD WAY (overlapping)
    x, y = 3, 3
    # Player 1 - Blue outer
    top_left = (x * cell_size, y * cell_size)
    bottom_right = ((x + 1) * cell_size - 1, (y + 1) * cell_size - 1)
    cv2.rectangle(board2, top_left, bottom_right, (255, 0, 0), 8)  # Blue
    
    # Player 2 - Red outer (same size - will overlap!)
    cv2.rectangle(board2, top_left, bottom_right, (0, 0, 255), 8)  # Red - overlaps!
    
    print("❌ Created board with overlapping cursors (problem)")
    
    # Test case 3: Cursors at same position - NEW WAY (nested)
    board3 = board.copy()
    
    # Both cursors at (3, 3) - NEW WAY (nested)
    x, y = 3, 3
    # Player 1 - Blue outer frame
    top_left_outer = (x * cell_size, y * cell_size)
    bottom_right_outer = ((x + 1) * cell_size - 1, (y + 1) * cell_size - 1)
    cv2.rectangle(board3, top_left_outer, bottom_right_outer, (255, 0, 0), 8)  # Blue outer
    
    # Player 2 - Red inner frame (smaller)
    margin = 10
    top_left_inner = (x * cell_size + margin, y * cell_size + margin)
    bottom_right_inner = ((x + 1) * cell_size - 1 - margin, (y + 1) * cell_size - 1 - margin)
    cv2.rectangle(board3, top_left_inner, bottom_right_inner, (0, 0, 255), 6)  # Red inner
    
    print("✅ Created board with nested cursors (solution)")
    
    # Add labels
    cv2.putText(board1, "Different Positions", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(board2, "Same Position - OLD", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(board3, "Same Position - NEW", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Combine all three boards horizontally
    combined = np.hstack([board1, board2, board3])
    
    # Show the result
    cv2.imshow("Cursor Visualization Test", combined)
    print("📺 Showing cursor visualization test. Press any key to close.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("🎉 Cursor visualization test completed!")

if __name__ == "__main__":
    test_cursor_visualization()
