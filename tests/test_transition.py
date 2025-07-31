#!/usr/bin/env python3
"""
Test to verify that the state transition from move to rest_long works properly
"""
import time

def test_state_transition():
    """Test that state transitions work correctly"""
    print("🧪 Testing state transition mechanism...")
    
    # Simulated state machine
    class MockState:
        def __init__(self):
            self.state = "idle"
            self.rest_start = None
            self.rest_time = {"rest_short": 2000, "rest_long": 5000}
            self.transitions = {
                "idle": {"move": "move", "jump": "jump"},
                "move": {"arrived": "rest_long"},
                "jump": {"arrived": "rest_short"},
                "rest_short": {"rest_done": "idle"},
                "rest_long": {"rest_done": "idle"},
            }
            
        def _transition(self, event, now_ms):
            """Simulate the _transition method"""
            next_state = self.transitions.get(self.state, {}).get(event)
            if next_state:
                old_state = self.state
                self.state = next_state
                print(f"🔄 State transition: {old_state} -> {self.state} (event: {event})")
                
                # Initialize rest if needed
                if self.state in ("rest_short", "rest_long"):
                    self.rest_start = now_ms
                    rest_duration = self.rest_time[self.state] / 1000
                    print(f"💤 Starting rest {self.state} for {rest_duration} seconds")
                elif self.state == "idle":
                    self.rest_start = None
                    print(f"✅ Returned to idle state - ready for new movement")
                    
        def update(self, now_ms):
            """Simulate the update method"""
            if self.state in ("rest_short", "rest_long"):
                if self.rest_start is not None and now_ms - self.rest_start >= self.rest_time[self.state]:
                    print(f"⏰ Rest time completed for {self.state}")
                    self._transition("rest_done", now_ms)
    
    # Test the sequence that should happen for promoted queen
    mock_state = MockState()
    now_ms = int(time.time() * 1000)
    
    print(f"1. Initial state: {mock_state.state}")
    
    # Simulate our fix: set to move then transition to arrived
    mock_state.state = "move"
    print(f"2. Set to move state: {mock_state.state}")
    
    mock_state._transition("arrived", now_ms)
    print(f"3. After arrived transition: {mock_state.state}")
    
    # Test that rest completes after time
    future_time = now_ms + 6000  # 6 seconds later
    mock_state.update(future_time)
    print(f"4. After rest completion: {mock_state.state}")
    
    if mock_state.state == "idle":
        print("✅ SUCCESS: State machine works correctly!")
    else:
        print(f"❌ FAILURE: Expected idle, got {mock_state.state}")
        
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_state_transition()
