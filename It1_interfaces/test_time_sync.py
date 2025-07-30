#!/usr/bin/env python3
"""
Test to verify that game time synchronization works correctly
"""
import time

def test_time_synchronization():
    """Test that our time matches the game's time method"""
    print("🧪 Testing time synchronization...")
    
    # Simulate the game's time method
    def game_time_ms():
        return int(time.monotonic() * 1000)
    
    # Compare different time methods
    time_time = int(time.time() * 1000)
    monotonic_time = int(time.monotonic() * 1000)
    game_time = game_time_ms()
    
    print(f"time.time() * 1000:      {time_time}")
    print(f"time.monotonic() * 1000: {monotonic_time}")
    print(f"game_time_ms():          {game_time}")
    
    # The difference between time.time() and time.monotonic() can be huge!
    diff = abs(time_time - monotonic_time)
    print(f"Difference: {diff}ms = {diff/1000/60:.1f} minutes")
    
    if diff > 60000:  # More than 1 minute difference
        print("❌ MAJOR TIME DIFFERENCE DETECTED!")
        print("   This explains why the rest timer never expires.")
        print("   time.time() and time.monotonic() have different epochs!")
    else:
        print("✅ Time methods are synchronized")
    
    # Test rest calculation with both methods
    rest_duration = 5000  # 5 seconds
    
    print(f"\n🧪 Testing rest timer calculation:")
    print(f"Rest duration: {rest_duration}ms")
    
    # Using time.time() (wrong way)
    start_time_wrong = time_time
    end_time_wrong = start_time_wrong + rest_duration
    print(f"Wrong way - Start: {start_time_wrong}, End should be: {end_time_wrong}")
    print(f"  Current monotonic time: {monotonic_time}")
    print(f"  Would rest complete? {monotonic_time >= end_time_wrong}")
    
    # Using monotonic time (correct way)  
    start_time_correct = monotonic_time
    end_time_correct = start_time_correct + rest_duration
    print(f"Correct way - Start: {start_time_correct}, End should be: {end_time_correct}")
    
    # Simulate a small time passage
    time.sleep(0.1)  # 100ms
    new_monotonic = int(time.monotonic() * 1000)
    print(f"  After 100ms, monotonic time: {new_monotonic}")
    print(f"  Would rest complete? {new_monotonic >= end_time_correct}")
    
    print("\n🎉 Time synchronization test completed!")

if __name__ == "__main__":
    test_time_synchronization()
