"""Digital Clock implementation with multiple timezone support."""

from datetime import datetime
from typing import List, Dict
from digital_clock.timezone_manager import TimezoneManager


class DigitalClock:
    """Digital clock that displays time in multiple timezones."""
    
    def __init__(self, default_timezones: List[str] = None):
        """Initialize the digital clock.
        
        Args:
            default_timezones: List of timezone display names to initialize with
        """
        self.timezone_manager = TimezoneManager()
        self.active_timezones: List[str] = []
        
        if default_timezones:
            for tz in default_timezones:
                self.add_timezone(tz)
        else:
            # Add some default timezones
            self.add_timezone("UTC")
            self.add_timezone("EST")
            self.add_timezone("JST")
    
    def add_timezone(self, name: str) -> bool:
        """Add a timezone to the clock display.
        
        Args:
            name: Display name of the timezone
            
        Returns:
            True if added successfully
        """
        if name not in self.active_timezones and name in self.timezone_manager.list_timezones():
            self.active_timezones.append(name)
            return True
        return False
    
    def remove_timezone(self, name: str) -> bool:
        """Remove a timezone from the clock display.
        
        Args:
            name: Display name of the timezone
            
        Returns:
            True if removed successfully
        """
        if name in self.active_timezones:
            self.active_timezones.remove(name)
            return True
        return False
    
    def register_custom_timezone(self, name: str, timezone_str: str) -> bool:
        """Register a custom timezone.
        
        Args:
            name: Display name for the timezone
            timezone_str: IANA timezone string
            
        Returns:
            True if registered successfully
        """
        return self.timezone_manager.add_timezone(name, timezone_str)
    
    def get_all_times(self) -> Dict[str, str]:
        """Get current time in all active timezones.
        
        Returns:
            Dictionary mapping timezone names to formatted time strings
        """
        times = {}
        for tz_name in self.active_timezones:
            dt = self.timezone_manager.get_time_in_timezone(tz_name)
            if dt:
                offset = self.timezone_manager.get_offset_string(tz_name)
                times[tz_name] = {
                    "time": dt.strftime("%H:%M:%S"),
                    "date": dt.strftime("%Y-%m-%d"),
                    "offset": offset,
                    "formatted": dt.strftime("%Y-%m-%d %H:%M:%S")
                }
        return times
    
    def get_time_in(self, timezone_name: str) -> Dict[str, str]:
        """Get time in a specific timezone.
        
        Args:
            timezone_name: Display name of the timezone
            
        Returns:
            Dictionary with time information
        """
        dt = self.timezone_manager.get_time_in_timezone(timezone_name)
        if not dt:
            return {}
        
        offset = self.timezone_manager.get_offset_string(timezone_name)
        return {
            "timezone": timezone_name,
            "time": dt.strftime("%H:%M:%S"),
            "date": dt.strftime("%Y-%m-%d"),
            "offset": offset,
            "formatted": dt.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def list_available_timezones(self) -> List[str]:
        """List all available timezones.
        
        Returns:
            List of available timezone names
        """
        return self.timezone_manager.list_timezones()
    
    def list_active_timezones(self) -> List[str]:
        """List currently active timezones on the clock.
        
        Returns:
            List of active timezone names
        """
        return sorted(self.active_timezones)


class ClockDisplay:
    """Format and display the digital clock."""
    
    def __init__(self, clock: DigitalClock):
        """Initialize the clock display.
        
        Args:
            clock: DigitalClock instance to display
        """
        self.clock = clock
    
    def display_simple(self) -> str:
        """Display clock in simple format.
        
        Returns:
            Formatted string with all active timezones
        """
        times = self.clock.get_all_times()
        output = []
        output.append("="*50)
        output.append("Digital Clock - Current Time".center(50))
        output.append("="*50)
        
        for tz_name in sorted(times.keys()):
            time_info = times[tz_name]
            line = f"{tz_name:12} | {time_info['time']} | {time_info['offset']}"
            output.append(line)
        
        output.append("="*50)
        return "\n".join(output)
    
    def display_detailed(self) -> str:
        """Display clock in detailed format.
        
        Returns:
            Formatted string with detailed time information
        """
        times = self.clock.get_all_times()
        output = []
        output.append("="*70)
        output.append("Digital Clock - Detailed Time Information".center(70))
        output.append("="*70)
        
        for tz_name in sorted(times.keys()):
            time_info = times[tz_name]
            output.append(f"\nTimezone: {tz_name}")
            output.append(f"  Date: {time_info['date']}")
            output.append(f"  Time: {time_info['time']}")
            output.append(f"  UTC Offset: {time_info['offset']}")
        
        output.append("\n" + "="*70)
        return "\n".join(output)
    
    def display_table(self) -> str:
        """Display clock in table format.
        
        Returns:
            Formatted table string
        """
        times = self.clock.get_all_times()
        
        output = []
        output.append("┌─────────────┬──────────────┬────────────┬─────────┐")
        output.append("│ Timezone    │ Date         │ Time       │ Offset  │")
        output.append("├─────────────┼──────────────┼────────────┼─────────┤")
        
        for tz_name in sorted(times.keys()):
            time_info = times[tz_name]
            tz = tz_name.ljust(11)
            date = time_info['date'].ljust(12)
            time = time_info['time'].ljust(10)
            offset = time_info['offset'].ljust(7)
            output.append(f"│ {tz} │ {date} │ {time} │ {offset} │")
        
        output.append("└─────────────┴──────────────┴────────────┴─────────┘")
        return "\n".join(output)
    
    def display_json(self) -> Dict:
        """Get clock data as dictionary (JSON-serializable).
        
        Returns:
            Dictionary with all clock data
        """
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "active_timezones": self.clock.list_active_timezones(),
            "times": self.clock.get_all_times()
        }
