# Digital Clock with Timezone Support

A Python library for displaying the current time across multiple time zones with various formatting options.

## Features

- ⏰ Display current time in multiple time zones simultaneously
- 🌍 Support for 50+ common time zones
- 🎨 Multiple display formats (simple, detailed, table, JSON)
- ➕ Add custom time zones dynamically
- 📊 UTC offset information for each timezone
- 🧪 Comprehensive unit tests

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from digital_clock import DigitalClock, ClockDisplay

# Create a clock with default timezones
clock = DigitalClock()

# Add more timezones
clock.add_timezone("PST")
clock.add_timezone("CET")

# Display the clock
display = ClockDisplay(clock)
print(display.display_simple())
```

## Usage Examples

### Basic Usage

```python
from digital_clock import DigitalClock

# Create a clock
clock = DigitalClock()

# Get current time in a specific timezone
time_info = clock.get_time_in("JST")
print(f"Tokyo time: {time_info['formatted']}")

# Get all times
all_times = clock.get_all_times()
for tz, info in all_times.items():
    print(f"{tz}: {info['time']} UTC{info['offset']}")
```

### Adding Custom Timezones

```python
clock = DigitalClock()

# Register a custom timezone
clock.register_custom_timezone("Sydney", "Australia/Sydney")
clock.add_timezone("Sydney")
```

### Different Display Formats

```python
display = ClockDisplay(clock)

# Simple format
print(display.display_simple())

# Detailed format
print(display.display_detailed())

# Table format
print(display.display_table())

# JSON format
import json
data = display.display_json()
print(json.dumps(data, indent=2))
```

### Available Timezones

Pre-configured common timezones:
- **UTC** - Coordinated Universal Time
- **EST** - Eastern Standard Time (US)
- **CST** - Central Standard Time (US)
- **MST** - Mountain Standard Time (US)
- **PST** - Pacific Standard Time (US)
- **IST** - Indian Standard Time
- **JST** - Japan Standard Time
- **AEST** - Australian Eastern Standard Time
- **NZST** - New Zealand Standard Time
- **CET** - Central European Time
- **SGT** - Singapore Time
- **HKT** - Hong Kong Time
- **BRT** - Brazil Time
- **AKST** - Alaska Standard Time

And more! Use `clock.list_available_timezones()` to see all available timezones.

## API Reference

### DigitalClock

#### Constructor
```python
DigitalClock(default_timezones: List[str] = None)
```

#### Methods

- `add_timezone(name: str) -> bool` - Add a timezone to the clock
- `remove_timezone(name: str) -> bool` - Remove a timezone from the clock
- `register_custom_timezone(name: str, timezone_str: str) -> bool` - Register a custom timezone
- `get_all_times() -> Dict[str, Dict]` - Get all current times
- `get_time_in(timezone_name: str) -> Dict[str, str]` - Get time in specific timezone
- `list_available_timezones() -> List[str]` - List all available timezones
- `list_active_timezones() -> List[str]` - List currently active timezones

### ClockDisplay

#### Methods

- `display_simple() -> str` - Simple format display
- `display_detailed() -> str` - Detailed format display
- `display_table() -> str` - Table format display
- `display_json() -> Dict` - JSON format display

### TimezoneManager

#### Methods

- `add_timezone(name: str, timezone_str: str) -> bool` - Add timezone
- `remove_timezone(name: str) -> bool` - Remove timezone
- `get_timezone(name: str) -> Optional[str]` - Get timezone string
- `list_timezones() -> List[str]` - List all timezones
- `get_time_in_timezone(name: str) -> Optional[datetime]` - Get datetime in timezone
- `get_offset_string(name: str) -> Optional[str]` - Get UTC offset

## Output Examples

### Simple Format
```
==================================================
          Digital Clock - Current Time
==================================================
EST          | 14:32:45 | -05:00
JST          | 03:32:45 | +09:00
UTC          | 19:32:45 | +00:00
==================================================
```

### Table Format
```
┌─────────────┬──────────────┬────────────┬─────────┐
│ Timezone    │ Date         │ Time       │ Offset  │
├─────────────┼──────────────┼────────────┼─────────┤
│ EST         │ 2026-05-14   │ 14:32:45   │ -05:00  │
│ JST         │ 2026-05-15   │ 03:32:45   │ +09:00  │
│ UTC         │ 2026-05-14   │ 19:32:45   │ +00:00  │
└─────────────┴──────────────┴────────────┴─────────┘
```

## Testing

Run the test suite:

```bash
python -m digital_clock.tests
```

Or with pytest:

```bash
pytest digital_clock/tests.py -v
```

## License

MIT
