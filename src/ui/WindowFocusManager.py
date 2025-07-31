"""
WindowFocusManager - Class for managing game window focus on Windows
Solves the issue where input is captured in VSCode instead of the game
"""
import cv2
import sys
import time
import ctypes
from ctypes import wintypes
from src.ui.window_utils import center_window


class WindowFocusManager:
    """Manages automatic window focus for the chess game"""
    
    def __init__(self, window_name: str = "Chess Game", window_position: str = "center"):
        self.window_name = window_name
        self.window_position = window_position  # "center" or "top-left"
        self.window_handle = None
        self.focus_attempts = 0
        self.max_focus_attempts = 3
        
        # Windows API functions
        try:
            self.user32 = ctypes.windll.user32
            self.kernel32 = ctypes.windll.kernel32
            self.windows_api_available = True
        except:
            self.windows_api_available = False
            print("⚠️ Windows API not available - focus management limited")
    
    def create_focused_window(self):
        """Create the game window with automatic focus"""
        try:
            # Create the window
            cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
            
            # Basic OpenCV settings
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 1)
            
            # Position window according to choice (estimated game window size)
            game_window_width = 800
            game_window_height = 800
            center_window(self.window_name, game_window_width, game_window_height, self.window_position)
            
            # Attempt to get automatic focus
            self.ensure_focus()
            
            print(f"🖥️ Game window '{self.window_name}' created with focus")
            return True
        except Exception as e:
            print(f"❌ Failed to create focused window: {e}")
            return False
    
    def ensure_focus(self):
        """Ensure the game window has focus"""
        if not self.windows_api_available:
            # Fallback to OpenCV methods only
            self._opencv_focus_fallback()
            return
        
        try:
            # Find the window
            if not self.window_handle:
                self.window_handle = self._find_window()
            
            if self.window_handle:
                # Bring window to front
                self.user32.SetForegroundWindow(self.window_handle)
                self.user32.SetActiveWindow(self.window_handle)
                self.user32.SetFocus(self.window_handle)
                
                # Ensure window is visible
                self.user32.ShowWindow(self.window_handle, 9)  # SW_RESTORE
                self.user32.BringWindowToTop(self.window_handle)
                
                return True
        except Exception as e:
            print(f"⚠️ Focus attempt failed: {e}")
            self._opencv_focus_fallback()
        
        return False
    
    def _find_window(self):
        """Find the OpenCV window handle"""
        try:
            # Try to find window by name
            hwnd = self.user32.FindWindowW(None, self.window_name)
            if hwnd:
                return hwnd
            
            # Alternative attempt - search OpenCV windows
            def enum_windows_proc(hwnd, lParam):
                length = self.user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    self.user32.GetWindowTextW(hwnd, buff, length + 1)
                    if self.window_name in buff.value:
                        self.window_handle = hwnd
                        return False  # Stop the search
                return True
            
            enum_windows_proc_type = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
            enum_proc = enum_windows_proc_type(enum_windows_proc)
            self.user32.EnumWindows(enum_proc, 0)
            
            return self.window_handle
        except:
            return None
    
    def _opencv_focus_fallback(self):
        """Fallback method using only OpenCV"""
        try:
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 1)
            time.sleep(0.01)  # Short wait
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 0)
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 1)
        except:
            pass
    
    def is_window_focused(self):
        """Check if the game window is currently focused"""
        if not self.windows_api_available or not self.window_handle:
            return False
        
        try:
            foreground_window = self.user32.GetForegroundWindow()
            return foreground_window == self.window_handle
        except:
            return False
    
    def smart_focus_check(self):
        """Smart focus check - only force focus if needed"""
        if self.is_window_focused():
            return True
        
        if self.focus_attempts < self.max_focus_attempts:
            self.focus_attempts += 1
            print(f"🎯 Auto-focusing game window (attempt {self.focus_attempts})")
            return self.ensure_focus()
        
        return False
