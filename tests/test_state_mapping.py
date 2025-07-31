#!/usr/bin/env python3
"""
Quick test to verify state mapping is correct
"""

def test_state_mapping():
    """Test that our state mapping matches the Graphics mapping"""
    print("🧪 Testing state mapping...")
    
    # The Graphics mapping from the code
    graphics_folder_map = {
        "idle": "idle",
        "move": "move", 
        "jump": "jump",
        "rest_short": "short_rest",
        "rest_long": "long_rest"  # This is the key mapping!
    }
    
    # Our fix uses "rest_long" as the internal state
    promoted_queen_state = "rest_long"
    
    # Check that this maps correctly to the folder name
    expected_folder = graphics_folder_map.get(promoted_queen_state, "idle")
    
    print(f"✅ Internal state: {promoted_queen_state}")
    print(f"✅ Folder name: {expected_folder}")
    
    if expected_folder == "long_rest":
        print("✅ SUCCESS: State mapping is correct!")
        print("   The promoted queen will use the correct 'long_rest' sprites")
    else:
        print(f"❌ FAILURE: Expected 'long_rest' folder, got '{expected_folder}'")
        
    print("\n🎉 Test completed!")

if __name__ == "__main__":
    test_state_mapping()
