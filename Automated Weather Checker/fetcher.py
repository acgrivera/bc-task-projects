import requests
import json
import logging
from logger import setup_logger


def fetch_weather(api_url,latitude,longitude,timezone):

    #setup_logger()
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly":"temperature_2m,relativehumidity_2m,windspeed_10m",
        "timezone":timezone
        }
    try:
        response = requests.get(api_url,params=params)
        if response.status_code == 200:
            logging.info("Weather data fetched successfully.")
            weather_data = response.json()
            return weather_data
        else:
            logging.error(f"Failed to fetch weather data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching weather data: {e}")
        return None
    
def save_raw(data,filename):
    #setup_logger()
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    logging.info("Raw data saved successfully.")