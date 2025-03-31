#!/usr/bin/env python3

import urllib.request
import json
from datetime import datetime, timedelta
import re


class TahajjudCalculator:
    def __init__(self):
        self.base_url = "http://api.aladhan.com/v1/timings"
        self.ip_api_url = "http://ip-api.com/json/"

    def validate_coordinates(self, latitude, longitude):
        """Validate if the coordinates are within valid ranges."""
        return -90 <= latitude <= 90 and -180 <= longitude <= 180

    def get_location(self):
        """Get user's location based on IP address."""
        try:
            with urllib.request.urlopen(self.ip_api_url) as response:
                data = json.loads(response.read().decode())
                if data["status"] == "success":
                    return {
                        "latitude": data["lat"],
                        "longitude": data["lon"],
                        "city": data["city"],
                        "country": data["country"]
                    }
                return None
        except Exception as e:
            print(f"Error getting location: {e}")
            return None

    def get_prayer_times(self, latitude, longitude, date=None):
        """Get prayer times for a specific location and date."""
        if not self.validate_coordinates(latitude, longitude):
            print("Invalid coordinates provided")
            return None

        if date is None:
            date = datetime.now().strftime("%d-%m-%Y")

        params = f"?latitude={latitude}&longitude={longitude}&method=5&date={date}"
        url = f"{self.base_url}{params}"

        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
                return data["data"]["timings"]
        except Exception as e:
            print(f"Error fetching prayer times: {e}")
            return None

    def get_next_day_prayer_times(self, latitude, longitude, date=None):
        """Get prayer times for the next day."""
        if date is None:
            date = datetime.now()
        tomorrow = (date + timedelta(days=1)).strftime("%d-%m-%Y")
        return self.get_prayer_times(latitude, longitude, tomorrow)

    def parse_time(self, time_str):
        """Parse time string into datetime object."""
        try:
            # Convert 24-hour time string to datetime
            hours, minutes = map(int, time_str.split(':'))
            now = datetime.now()
            return datetime(now.year, now.month, now.day, hours, minutes)
        except (ValueError, TypeError) as e:
            print(f"Error parsing time {time_str}: {e}")
            return None

    def format_duration(self, duration):
        """Format timedelta into hours and minutes."""
        total_minutes = int(duration.total_seconds() / 60)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours}h {minutes}m"

    def calculate_tahajjud_schedule(self, isha_time, fajr_time):
        """Calculate Tahajjud prayer schedule based on Isha and Fajr times."""
        # Convert times to datetime objects
        isha = self.parse_time(isha_time)
        fajr = self.parse_time(fajr_time)

        if not isha or not fajr:
            return None

        # Fajr is always on the next day, so add 24 hours
        fajr += timedelta(days=1)

        # Calculate night duration
        night_duration = fajr - isha

        # Calculate schedule
        half_night = night_duration / 2
        third_night = night_duration / 3
        sixth_night = night_duration / 6

        # Calculate times
        sleep_start = isha
        tahajjud_start = sleep_start + half_night
        tahajjud_end = tahajjud_start + third_night
        second_sleep_start = tahajjud_end
        second_sleep_end = fajr

        return {
            "first_sleep": {
                "start": sleep_start.strftime("%H:%M"),
                "end": tahajjud_start.strftime("%H:%M"),
                "duration": self.format_duration(half_night)
            },
            "tahajjud": {
                "start": tahajjud_start.strftime("%H:%M"),
                "end": tahajjud_end.strftime("%H:%M"),
                "duration": self.format_duration(third_night)
            },
            "second_sleep": {
                "start": second_sleep_start.strftime("%H:%M"),
                "end": second_sleep_end.strftime("%H:%M"),
                "duration": self.format_duration(sixth_night)
            },
            "fajr": fajr.strftime("%H:%M"),
            "total_night_duration": self.format_duration(night_duration)
        }

    def get_schedule(self, latitude=None, longitude=None, date=None):
        """Get complete Tahajjud schedule for a location."""
        # If no coordinates provided, try to get them from IP
        if latitude is None or longitude is None:
            location = self.get_location()
            if location:
                latitude = location["latitude"]
                longitude = location["longitude"]
            else:
                print(
                    "Could not determine location. Please provide coordinates manually.")
                return None

        # Get current day's Isha and next day's Fajr
        current_times = self.get_prayer_times(latitude, longitude, date)
        next_day_times = self.get_next_day_prayer_times(
            latitude, longitude, date)

        if not current_times or not next_day_times:
            return None

        schedule = self.calculate_tahajjud_schedule(
            current_times["Isha"],
            next_day_times["Fajr"]
        )

        return schedule

    def print_schedule(self, schedule, location=None):
        """Print the schedule in a formatted way."""
        if not schedule:
            print("Failed to calculate schedule")
            return

        if location:
            print(f"\nLocation: {location['city']}, {location['country']}")
            print(
                f"Coordinates: {location['latitude']}, {location['longitude']}")

        print("\nTahajjud Prayer Schedule:")
        print("-------------------------")
        print(f"Total Night Duration: {schedule['total_night_duration']}")
        print(
            f"First Sleep: {schedule['first_sleep']['start']} - {schedule['first_sleep']['end']} ({schedule['first_sleep']['duration']})")
        print(
            f"Tahajjud Prayer: {schedule['tahajjud']['start']} - {schedule['tahajjud']['end']} ({schedule['tahajjud']['duration']})")
        print(
            f"Second Sleep: {schedule['second_sleep']['start']} - {schedule['second_sleep']['end']} ({schedule['second_sleep']['duration']})")
        print(f"Fajr Prayer: {schedule['fajr']}")


def main():
    calculator = TahajjudCalculator()

    # Get location automatically
    location = calculator.get_location()
    if location:
        schedule = calculator.get_schedule(
            location["latitude"], location["longitude"])
        calculator.print_schedule(schedule, location)
    else:
        print("Failed to get location")
        return


if __name__ == "__main__":
    main()
