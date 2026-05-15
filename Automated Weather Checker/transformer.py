import logging
import json

def transform_data(raw_data):
    try:
        hourly = raw_data["hourly"]
        time = hourly["time"]
        temperature = hourly["temperature_2m"]
        humidity = hourly["relativehumidity_2m"]
        windspeed = ["windspeed_10m"]
        cleaned_data = []

        for i in range(len(time)):
            record = {
                "timestamp": time[i],
                "temperature": temperature[i],
            }
            cleaned_data.append(record)
        logging.info(f"Transformed {len(cleaned_data)} records,")
        return cleaned_data
    except KeyError as e:
        logging.error(f"Unexpected API format: {e}")
        return None
    
def save_clean_data(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    logging.info("Clean data saved successfully.")

def generate_summary(records):
    if not records:
        return None
    temperatures = [record["temperature"] for record in records]
    summary = {
        "record_count": len(records),
        "average_temperature": sum(temperatures) / len(temperatures),
        "min_temperature": min(temperatures),
        "max_temperature": max(temperatures)
    }
    logging.info("Summary generated successfully.")
    return summary

def save_summary(summary, filename):
    with open(filename, 'w') as file:
        json.dump(summary, file, indent=4)
    logging.info("Summary saved successfully.")