import json
import logging
from logger import setup_logger
from fetcher import fetch_weather, save_raw
from transformer import transform_data, save_clean_data, generate_summary, save_summary


def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def main():
    setup_logger()
    config = load_config('config.json')

    logging.info("Weather Pipeline started.")

    raw_data = fetch_weather(config['api_url'],
                             config['latitude'],
                             config['longitude'],
                             config['timezone']
                             )
    if not raw_data:
        logging.error("Failed to fetch weather data.")
        return
    save_raw(raw_data, config["raw_output"])
    cleaned = transform_data(raw_data)
    save_clean_data(cleaned, config["clean_output"])
    summary = generate_summary(cleaned)
    save_summary(summary, config["summary_output"])

if __name__ == "__main__":
    main()                        