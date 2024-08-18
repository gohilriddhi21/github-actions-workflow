import logging
import logging.handlers
import os
import requests


def setup_logger(file_name):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        file_name,
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)
    return logger


def get_api_key(logger):
    try:
        WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
        logger.info("API KEY set successfully.")
        return WEATHER_API_KEY
    except KeyError:
        logger.info("Key not available!")
        raise


def fetch_weather(api_key, location="Seattle"):
    BASE_URL = "http://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": location, "aqi": "no"}

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def log_weather_data(logger, weather_data):
    location = weather_data["location"]["name"]
    region = weather_data["location"]["region"]
    temperature = weather_data["current"]["temp_c"]
    time = weather_data["location"]["localtime"]
    logger.info(f"Weather in {location},{region} at {time}: {temperature}")


def main():
    logger = setup_logger("status.log")
    try:
        api_key = get_api_key(logger)
        response_data = fetch_weather(api_key, location="New York")
        log_weather_data(logger, response_data)
    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
