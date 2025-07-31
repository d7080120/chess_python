"""
Window positioning utilities for centering windows on screen
"""
import cv2


def get_screen_center_position(window_width, window_height):
    """
    Calculate center position for a window on the screen
    
    Args:
        window_width: Width of the window
        window_height: Height of the window
        
    Returns:
        tuple: (center_x, center_y) position for the window
    """
    try:
        import tkinter as tk
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        
        # Calculate perfect center position
        center_x = (screen_width - window_width) // 2
        center_y = (screen_height - window_height) // 2
        
        # Ensure window doesn't go off screen
        center_x = max(0, center_x)
        center_y = max(0, center_y)
        
        return center_x, center_y
        
    except Exception as e:
        print(f"⚠️ Could not get screen dimensions: {e}")
        # Default approximate center
        return 200, 100


def get_top_left_position():
    """
    Get top-left corner position for a window
    
    Returns:
        tuple: (0, 0) for top-left corner
    """
    return 0, 0


def center_window(window_name, window_width, window_height, position="center"):
    """
    Move an OpenCV window to a specified position on the screen
    
    Args:
        window_name: Name of the OpenCV window
        window_width: Width of the window
        window_height: Height of the window
        position: "center" for screen center, "top-left" for top-left corner
    """
    try:
        if position == "top-left":
            pos_x, pos_y = get_top_left_position()
            print(f"🖥️ Window '{window_name}' positioned at top-left corner (0, 0)")
        else:  # default to center
            pos_x, pos_y = get_screen_center_position(window_width, window_height)
            print(f"🖥️ Window '{window_name}' centered at ({pos_x}, {pos_y})")
        
        cv2.moveWindow(window_name, pos_x, pos_y)
        return True
    except Exception as e:
        print(f"⚠️ Could not position window '{window_name}': {e}")
        return False
