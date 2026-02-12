"""OpenWeatherMap API Pipeline - Core extraction logic"""

import logging
from datetime import datetime
from typing import Any

import requests

logger = logging.getLogger(__name__)


class OpenWeatherAPIClient:
    """Client for OpenWeatherMap API interactions."""

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str):
        """Initialize with API key."""
        self.api_key = api_key
        self.headers = {
            "User-Agent": "DEX-Weather-Pipeline/1.0",
            "Accept": "application/json",
        }

    def get_weather(self, city: str, units: str = "metric") -> dict[str, Any]:
        """
        Fetch current weather for a city.

        Args:
            city: City name
            units: Temperature units (metric, imperial, kelvin)

        Returns:
            Weather data dictionary
        """
        endpoint = f"{self.BASE_URL}/weather"
        params = {"q": city, "units": units, "appid": self.api_key}

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch weather for {city}: {str(e)}")
            raise


class OpenWeatherPipeline:
    """Main pipeline for weather data extraction and transformation."""

    def __init__(self, api_key: str):
        """Initialize pipeline with API credentials."""
        self.client = OpenWeatherAPIClient(api_key)
        self.extracted_data = []

    def extract_cities(
        self, cities: list[str], units: str = "metric"
    ) -> list[dict[str, Any]]:
        """
        Extract weather data for multiple cities.

        Args:
            cities: List of city names
            units: Temperature units

        Returns:
            List of extracted weather records
        """
        logger.info(f"Extracting weather for {len(cities)} cities")
        self.extracted_data = []

        for city in cities:
            try:
                data = self.client.get_weather(city, units)
                record = self._transform_record(data)
                self.extracted_data.append(record)
                logger.info(f"✓ {city}: {record['temperature']}°C")
            except requests.exceptions.RequestException as e:
                logger.error(f"✗ {city}: {str(e)}")
                continue

        return self.extracted_data

    def _transform_record(self, api_response: dict[str, Any]) -> dict[str, Any]:
        """Transform raw API response to standardized format."""
        weather = api_response["weather"][0]
        visibility_km = api_response.get("visibility", 0) / 1000
        return {
            "city": api_response["name"],
            "country": api_response["sys"]["country"],
            "temperature": api_response["main"]["temp"],
            "feels_like": api_response["main"]["feels_like"],
            "humidity": api_response["main"]["humidity"],
            "pressure": api_response["main"]["pressure"],
            "condition": weather["main"],
            "description": weather["description"],
            "wind_speed": api_response["wind"]["speed"],
            "visibility": visibility_km,
            "cloudiness": api_response["clouds"]["all"],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def validate(self) -> bool:
        """Validate extracted data quality."""
        if not self.extracted_data:
            logger.warning("No data extracted")
            return False

        required_fields = ["city", "temperature", "humidity", "condition"]
        for record in self.extracted_data:
            for field in required_fields:
                if field not in record or record[field] is None:
                    city = record.get("city", "Unknown")
                    logger.error(f"Missing {field} in {city}")
                    return False

        count = len(self.extracted_data)
        logger.info(f"✓ Data validation passed for {count} records")
        return True

    def get_data(self) -> list[dict[str, Any]]:
        """Get extracted and transformed data."""
        return self.extracted_data
