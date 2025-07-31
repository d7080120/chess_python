#!/usr/bin/env python3
"""
Test to debug the queen rest transition issue
"""
import time

def test_debug_rest_transition():
    """Debug test for rest transition issue"""
    print("🧪 Debugging rest transition mechanism...")
    
    # Simulated state machine with the same logic as the real State class
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
            else:
                print(f"❌ No transition found for {self.state} -> {event}")
                    
        def update(self, now_ms):
            """Simulate the update method with detailed debugging"""
            print(f"🔄 Update called: state={self.state}, now={now_ms}")
            
            if self.state in ("rest_short", "rest_long"):
                if self.rest_start is not None:
                    elapsed = now_ms - self.rest_start
                    required = self.rest_time[self.state]
                    remaining = required - elapsed
                    
                    print(f"   Rest: elapsed={elapsed}ms, required={required}ms, remaining={remaining}ms")
                    
                    if elapsed >= required:
                        print(f"⏰ DEBUG: Rest completed for {self.state} - transitioning to idle")
                        self._transition("rest_done", now_ms)
                        return True  # State changed
                    else:
                        print(f"💤 DEBUG: Still resting in {self.state}, {remaining}ms remaining")
                else:
                    print("⚠️ WARNING: In rest state but no rest_start time!")
            else:
                print(f"   Not in rest state - state is {self.state}")
                
            return False  # No state change
    
    # Test the exact sequence that happens for promoted queen
    mock_state = MockState()
    start_time = int(time.time() * 1000)
    
    print("=== SIMULATING QUEEN PROMOTION ===")
    print(f"1. Initial state: {mock_state.state}")
    
    # Our fix: set to move then transition to arrived
    mock_state.state = "move"
    print(f"2. Set to move state: {mock_state.state}")
    
    mock_state._transition("arrived", start_time)
    print(f"3. After arrived transition: {mock_state.state}")
    print(f"   Rest start time: {mock_state.rest_start}")
    
    # Test update calls over time
    print("\n=== SIMULATING GAME LOOP UPDATES ===")
    for i in range(10):  # Simulate 10 updates over time
        test_time = start_time + (i * 1000)  # Every second
        print(f"\nUpdate {i+1} at time {test_time}:")
        changed = mock_state.update(test_time)
        print(f"   Current state: {mock_state.state}, changed: {changed}")
        
        if mock_state.state == "idle":
            print("✅ SUCCESS: Queen reached idle state!")
            break
        elif i == 9:
            print("❌ FAILURE: Queen never reached idle state!")
    
    print("\n🎉 Debug test completed!")

if __name__ == "__main__":
    test_debug_rest_transition()
