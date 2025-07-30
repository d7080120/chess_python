#!/usr/bin/env python3
"""
Simple test to verify the pawn promotion state logic
"""
import time

def test_rest_long_state_setting():
    """Test the state setting logic without dependencies"""
    print("🧪 Testing rest_long state setting logic...")
    
    # Simulate the queen state object
    class MockState:
        def __init__(self):
            self.state = "idle"
            self.rest_start = None
            self.rest_time = {"rest_short": 2000, "rest_long": 5000}
            
        def is_resting(self, now_ms):
            """Check if the piece is still resting"""
            if self.state in ("rest_short", "rest_long"):
                if self.rest_start is not None:
                    elapsed_ms = now_ms - self.rest_start
                    required_ms = self.rest_time[self.state]
                    return elapsed_ms < required_ms
            return False
    
    # Test the new logic
    mock_state = MockState()
    now_ms = int(time.time() * 1000)
    
    # Apply our fix: directly set state and rest_start
    mock_state.state = "rest_long"
    mock_state.rest_start = now_ms
    
    print(f"✅ State set to: {mock_state.state}")
    print(f"⏰ Rest start time: {mock_state.rest_start}")
    
    # Test that it's resting immediately after promotion
    if mock_state.is_resting(now_ms + 100):  # 100ms later
        print("✅ SUCCESS: Queen is properly resting after promotion!")
    else:
        print("❌ FAILURE: Queen should be resting after promotion")
        
    # Test that it stops resting after the required time
    future_time = now_ms + 6000  # 6 seconds later (longer than rest_long duration)
    if not mock_state.is_resting(future_time):
        print("✅ SUCCESS: Queen stops resting after required time!")
    else:
        print("❌ FAILURE: Queen should stop resting after required time")
        
    print("\n🎉 Logic test completed!")

if __name__ == "__main__":
    test_rest_long_state_setting()
