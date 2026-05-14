"""Unit tests for digital clock."""

import unittest
from datetime import datetime
from digital_clock.clock import DigitalClock, ClockDisplay
from digital_clock.timezone_manager import TimezoneManager


class TestTimezoneManager(unittest.TestCase):
    """Test cases for TimezoneManager."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.manager = TimezoneManager()
    
    def test_get_timezone(self):
        """Test getting timezone string."""
        utc_tz = self.manager.get_timezone("UTC")
        self.assertEqual(utc_tz, "UTC")
    
    def test_list_timezones(self):
        """Test listing available timezones."""
        timezones = self.manager.list_timezones()
        self.assertIn("UTC", timezones)
        self.assertIn("EST", timezones)
        self.assertIn("JST", timezones)
    
    def test_add_custom_timezone(self):
        """Test adding custom timezone."""
        result = self.manager.add_timezone("MyTZ", "America/New_York")
        self.assertTrue(result)
        self.assertIn("MyTZ", self.manager.list_timezones())
    
    def test_add_invalid_timezone(self):
        """Test adding invalid timezone."""
        result = self.manager.add_timezone("InvalidTZ", "Invalid/Timezone")
        self.assertFalse(result)
    
    def test_remove_timezone(self):
        """Test removing timezone."""
        self.manager.add_timezone("TestTZ", "America/New_York")
        result = self.manager.remove_timezone("TestTZ")
        self.assertTrue(result)
        self.assertNotIn("TestTZ", self.manager.list_timezones())
    
    def test_get_time_in_timezone(self):
        """Test getting time in timezone."""
        dt = self.manager.get_time_in_timezone("UTC")
        self.assertIsNotNone(dt)
        self.assertIsInstance(dt, datetime)
    
    def test_get_offset_string(self):
        """Test getting UTC offset string."""
        offset = self.manager.get_offset_string("UTC")
        self.assertEqual(offset, "+00:00")


class TestDigitalClock(unittest.TestCase):
    """Test cases for DigitalClock."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.clock = DigitalClock()
    
    def test_initialization(self):
        """Test clock initialization."""
        self.assertGreater(len(self.clock.list_active_timezones()), 0)
    
    def test_add_timezone(self):
        """Test adding timezone to clock."""
        initial_count = len(self.clock.list_active_timezones())
        self.clock.add_timezone("PST")
        final_count = len(self.clock.list_active_timezones())
        self.assertEqual(final_count, initial_count + 1)
    
    def test_remove_timezone(self):
        """Test removing timezone from clock."""
        self.clock.add_timezone("PST")
        initial_count = len(self.clock.list_active_timezones())
        self.clock.remove_timezone("PST")
        final_count = len(self.clock.list_active_timezones())
        self.assertEqual(final_count, initial_count - 1)
    
    def test_register_custom_timezone(self):
        """Test registering custom timezone."""
        result = self.clock.register_custom_timezone("BuenosAires", "America/Argentina/Buenos_Aires")
        self.assertTrue(result)
        self.clock.add_timezone("BuenosAires")
        self.assertIn("BuenosAires", self.clock.list_active_timezones())
    
    def test_get_all_times(self):
        """Test getting all times."""
        times = self.clock.get_all_times()
        self.assertIsInstance(times, dict)
        self.assertGreater(len(times), 0)
        
        for tz_name, time_info in times.items():
            self.assertIn("time", time_info)
            self.assertIn("date", time_info)
            self.assertIn("offset", time_info)
    
    def test_get_time_in_specific_timezone(self):
        """Test getting time in specific timezone."""
        time_info = self.clock.get_time_in("UTC")
        self.assertIsNotNone(time_info)
        self.assertIn("time", time_info)
        self.assertIn("date", time_info)
        self.assertEqual(time_info["timezone"], "UTC")


class TestClockDisplay(unittest.TestCase):
    """Test cases for ClockDisplay."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.clock = DigitalClock()
        self.display = ClockDisplay(self.clock)
    
    def test_display_simple(self):
        """Test simple display format."""
        output = self.display.display_simple()
        self.assertIsInstance(output, str)
        self.assertIn("Digital Clock", output)
        self.assertIn("UTC", output)
    
    def test_display_detailed(self):
        """Test detailed display format."""
        output = self.display.display_detailed()
        self.assertIsInstance(output, str)
        self.assertIn("Timezone:", output)
    
    def test_display_table(self):
        """Test table display format."""
        output = self.display.display_table()
        self.assertIsInstance(output, str)
        self.assertIn("┌", output)  # Table corner character
    
    def test_display_json(self):
        """Test JSON display format."""
        data = self.display.display_json()
        self.assertIsInstance(data, dict)
        self.assertIn("timestamp", data)
        self.assertIn("active_timezones", data)
        self.assertIn("times", data)


if __name__ == "__main__":
    unittest.main()
