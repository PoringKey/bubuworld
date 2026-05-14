"""Timezone management for the digital clock."""

from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Dict, Optional


class TimezoneManager:
    """Manage and validate timezones."""
    
    # Common timezones with their UTC offsets and descriptions
    COMMON_TIMEZONES = {
        "UTC": "UTC",
        "GMT": "Europe/London",
        "EST": "US/Eastern",
        "CST": "US/Central",
        "MST": "US/Mountain",
        "PST": "US/Pacific",
        "IST": "Asia/Kolkata",
        "JST": "Asia/Tokyo",
        "AEST": "Australia/Sydney",
        "NZST": "Pacific/Auckland",
        "CET": "Europe/Paris",
        "SGT": "Asia/Singapore",
        "HKT": "Asia/Hong_Kong",
        "BRT": "America/Sao_Paulo",
        "AKST": "US/Alaska",
    }
    
    def __init__(self):
        """Initialize the timezone manager."""
        self.timezones: Dict[str, str] = self.COMMON_TIMEZONES.copy()
    
    def add_timezone(self, name: str, timezone_str: str) -> bool:
        """Add a custom timezone.
        
        Args:
            name: Display name for the timezone
            timezone_str: IANA timezone string (e.g., 'America/New_York')
            
        Returns:
            True if added successfully, False if invalid timezone
        """
        try:
            ZoneInfo(timezone_str)
            self.timezones[name] = timezone_str
            return True
        except Exception:
            return False
    
    def remove_timezone(self, name: str) -> bool:
        """Remove a timezone from the manager.
        
        Args:
            name: Display name of the timezone to remove
            
        Returns:
            True if removed, False if not found
        """
        if name in self.timezones:
            del self.timezones[name]
            return True
        return False
    
    def get_timezone(self, name: str) -> Optional[str]:
        """Get timezone string by name.
        
        Args:
            name: Display name of the timezone
            
        Returns:
            IANA timezone string or None if not found
        """
        return self.timezones.get(name)
    
    def list_timezones(self) -> List[str]:
        """Get list of all timezone names.
        
        Returns:
            List of timezone display names
        """
        return sorted(list(self.timezones.keys()))
    
    def get_time_in_timezone(self, name: str) -> Optional[datetime]:
        """Get current time in a specific timezone.
        
        Args:
            name: Display name of the timezone
            
        Returns:
            datetime object in the specified timezone or None if invalid
        """
        tz_str = self.get_timezone(name)
        if not tz_str:
            return None
        
        try:
            tz = ZoneInfo(tz_str)
            return datetime.now(tz)
        except Exception:
            return None
    
    def get_offset_string(self, name: str) -> Optional[str]:
        """Get UTC offset string for a timezone.
        
        Args:
            name: Display name of the timezone
            
        Returns:
            UTC offset string (e.g., '+05:30') or None if invalid
        """
        dt = self.get_time_in_timezone(name)
        if not dt:
            return None
        
        offset = dt.strftime("%z")
        if offset:
            return f"{offset[:3]}:{offset[3:]}"
        return None
