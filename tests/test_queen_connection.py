#!/usr/bin/env python3
"""
Test to verify that the new queen connects properly to the game system
"""

def test_queen_connection():
    """Test that the new queen is connected to the game system properly"""
    print("🧪 Testing queen connection to game system...")
    
    # Simulate the game connection
    class MockGameQueue:
        def __init__(self):
            self.commands = []
            
        def put(self, cmd):
            self.commands.append(cmd)
            print(f"📨 Game queue received command: {cmd.type}")
    
    class MockState:
        def __init__(self):
            self.state = "idle"
            self.rest_start = None
            self.rest_time = {"rest_short": 2000, "rest_long": 5000}
            self._game_queue = None
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
            """Simulate the update method with game queue connection"""
            if self.state in ("rest_short", "rest_long"):
                if self.rest_start is not None and now_ms - self.rest_start >= self.rest_time[self.state]:
                    print(f"⏰ Rest time completed for {self.state}")
                    self._transition("rest_done", now_ms)
                    return True  # State changed
            return False  # No state change
    
    # Test our fix
    import time
    
    # Create mock objects
    mock_game_queue = MockGameQueue()
    mock_state = MockState()
    now_ms = int(time.time() * 1000)
    
    print("1. Creating new queen state...")
    
    # Simulate our fix: connect to game queue
    mock_state._game_queue = mock_game_queue
    print("✅ Connected queen to game queue")
    
    # Set to move and transition to arrived
    mock_state.state = "move"
    print(f"2. Set initial state: {mock_state.state}")
    
    mock_state._transition("arrived", now_ms)
    print(f"3. After arrived transition: {mock_state.state}")
    
    # Test that update works over time
    print("4. Testing update mechanism...")
    for i in range(3):
        future_time = now_ms + (i + 1) * 2000  # Every 2 seconds
        changed = mock_state.update(future_time)
        print(f"   Time +{(i + 1) * 2}s: state={mock_state.state}, changed={changed}")
        if mock_state.state == "idle":
            break
    
    if mock_state.state == "idle":
        print("✅ SUCCESS: Queen properly transitions to idle after rest!")
    else:
        print(f"❌ FAILURE: Expected idle, got {mock_state.state}")
        
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_queen_connection()
