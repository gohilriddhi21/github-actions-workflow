""" Simple Flask Application to check the weather of any city. """
import logging
import logging.handlers
import os
import requests


def setup_logger(file_name):
    """Sets up a logger configuration.

    Args:
        file_name (str): The name of the log file that will be created.

    Returns:
        logging.Logger: Configured logger instance.
    """
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
    """Retrieves the weather API key from environment secret variables set in GitHub.

    Args:
        logger (logging.Logger): The logger instance to log messages.

    Returns:
        str: Weather API key as a string.

    Raises:
        KeyError: If the weather_api_key environment variable is not set.
    """
    try:
        weather_api_key = os.environ["WEATHER_API_KEY"]
        logger.info("API KEY set successfully.")
        return weather_api_key
    except KeyError:
        logger.info("Key not available!")
        raise


def fetch_weather(api_key, location="Seattle"):
    """Fetches the weather data for a given location using the provided API key.

    Args:
        api_key (str): The API key for authenticating the request.
        location (str, optional): The location to fetch the weather data for. Defaults to "Seattle".

    Returns:
        dict: Parsed JSON response containing weather information.

    Raises:
        requests.HTTPError: If the API request fails.
    """
    base_url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": location, "aqi": "no"}

    response = requests.get(base_url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()



def log_weather_data(logger, weather_data):
    """Logs the weather data.

    Args:
        logger (logging.Logger): The logger instance to log messages.
        weather_data (dict): The JSON response containing the weather data.
    """
    location = weather_data["location"]["name"]
    region = weather_data["location"]["region"]
    temperature = weather_data["current"]["temp_c"]
    time = weather_data["location"]["localtime"]
    logger.info(f"Weather in {location},{region} at {time}: {temperature}")


def main():
    """ Entrypoint of the application. """
    logger = setup_logger("status.log")
    try:
        api_key = get_api_key(logger)
        response_data = fetch_weather(api_key, location="New York")
        log_weather_data(logger, response_data)
    except KeyError as e:
        logger.error("An error occurred due to missing environment variable: %s", e)
    except requests.RequestException as e:
        logger.error("An error occurred while making the API request: %s", e)
    except Exception as e: # pylint: disable=W0718
        logger.error("An unexpected error occurred: %s", e)


if __name__ == "__main__":
    main()
