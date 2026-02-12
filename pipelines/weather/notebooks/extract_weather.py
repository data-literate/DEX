# Databricks notebook source

# MAGIC %md
# MAGIC # Weather Data - Extract
# MAGIC Extract current weather data from OpenWeatherMap API

# COMMAND ----------

import logging
from datetime import datetime

import requests
from pyspark.sql import SparkSession

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# COMMAND ----------

# Configuration
CITIES = "London,New York,Tokyo,Sydney"
UNITS = "metric"

# Get API key from Databricks secrets
api_key = dbutils.secrets.get(scope="dex", key="openweather_api_key")
logger.info("API key loaded from secrets")

# COMMAND ----------


def fetch_weather(city: str, api_key: str, units: str = "metric") -> dict:
    """Fetch weather data for a city."""
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "units": units, "appid": api_key}

    response = requests.get(endpoint, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def transform_record(api_response: dict) -> dict:
    """Transform API response to standard format."""
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


# COMMAND ----------

# Extract data for all cities
cities_list = [c.strip() for c in CITIES.split(",")]
weather_records = []

for city in cities_list:
    try:
        api_data = fetch_weather(city, api_key, UNITS)
        record = transform_record(api_data)
        weather_records.append(record)
        logger.info(f"✓ {city}: {record['temperature']}°C")
    except requests.exceptions.RequestException as e:
        logger.error(f"✗ {city}: API error - {str(e)}")
    except KeyError as e:
        logger.error(f"✗ {city}: Missing field - {str(e)}")

# COMMAND ----------

# Create DataFrame and save to Delta table
spark = SparkSession.builder.appName("WeatherExtract").getOrCreate()
df = spark.createDataFrame(weather_records)

# Write to a temporary Delta table that persists for this job
df.write.mode("overwrite").option("mergeSchema", "true").saveAsTable("weather_raw_temp")

logger.info(
    f"Extracted {len(weather_records)} weather records to weather_raw_temp table"
)
display(df)
