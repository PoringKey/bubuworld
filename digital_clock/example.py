"""Example usage of the digital clock."""

from digital_clock import DigitalClock, ClockDisplay
import json

def main():
    """Run digital clock examples."""
    
    print("\n" + "="*70)
    print("Digital Clock - Example Usage".center(70))
    print("="*70 + "\n")
    
    # Create a clock with custom timezones
    clock = DigitalClock(["UTC", "EST", "JST", "CET", "PST"])
    
    # Create display
    display = ClockDisplay(clock)
    
    # Example 1: Simple display
    print("\n1. SIMPLE FORMAT:")
    print(display.display_simple())
    
    # Example 2: Detailed display
    print("\n2. DETAILED FORMAT:")
    print(display.display_detailed())
    
    # Example 3: Table display
    print("\n3. TABLE FORMAT:")
    print(display.display_table())
    
    # Example 4: Add custom timezone
    print("\n4. ADDING CUSTOM TIMEZONE:")
    clock.register_custom_timezone("Sydney", "Australia/Sydney")
    clock.add_timezone("Sydney")
    print(f"Added Sydney timezone")
    print(display.display_simple())
    
    # Example 5: Get specific timezone time
    print("\n5. SPECIFIC TIMEZONE TIME:")
    time_info = clock.get_time_in("Sydney")
    print(f"Sydney: {time_info['formatted']} (UTC{time_info['offset']})")
    
    # Example 6: List available timezones
    print("\n6. AVAILABLE TIMEZONES:")
    available = clock.list_available_timezones()
    print(f"Total available timezones: {len(available)}")
    print(f"First 10: {', '.join(available[:10])}")
    
    # Example 7: JSON output
    print("\n7. JSON OUTPUT:")
    json_data = display.display_json()
    print(json.dumps(json_data, indent=2))

if __name__ == "__main__":
    main()
