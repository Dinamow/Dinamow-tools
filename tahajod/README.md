# Tahajjud Prayer Time Calculator

This tool helps you calculate the optimal times for Tahajjud prayer based on your location. It uses the Aladhan API to get accurate prayer times and calculates the best schedule for Tahajjud prayer according to Islamic traditions.

## Features

- Automatically detects your location based on IP address
- Shows your city and country
- Calculates prayer times based on your detected location
- Provides a complete schedule for:
  - First sleep period (half of the night)
  - Tahajjud prayer time (third of the night)
  - Second sleep period (sixth of the night)
  - Fajr prayer time
- Uses only built-in Python libraries (no external dependencies)

## Usage

Run the script with:
```bash
python tahajjud_calculator.py
```

The tool will automatically detect your location and show you the Tahajjud schedule for your area. If automatic location detection fails, you can still provide coordinates manually:

```python
from tahajjud_calculator import TahajjudCalculator

calculator = TahajjudCalculator()
schedule = calculator.get_schedule(latitude, longitude)  # Optional parameters
```

## API Reference

The tool uses two free APIs that don't require API keys:
- Aladhan API (http://api.aladhan.com) for prayer times
- IP-API (http://ip-api.com) for location detection

## Calculation Method

The schedule is calculated as follows:
1. Night duration is from Isha to Fajr
2. First half of the night is for sleep
3. Third of the night is for Tahajjud prayer
4. Remaining sixth of the night is for sleep again
5. Fajr prayer time is at the end 