import logging
import logging.handlers
import os
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
except KeyError:
    WEATHER_API_KEY = "Key not available!"
    logger.info("Key not available!")
    raise


if __name__ == "__main__":
    logger.info("API KEY set successfully.")
    
    BASE_URL = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": "Seattle", 
        "aqi": "no"  
    }
    
    r = requests.get(BASE_URL, params=params)
    if r.status_code == 200:
        data = r.json()
        location = data['location']['name']
        region = data['location']['region']
        temperature = data['current']['temp_c']
        time = data['location']['localtime']
        logger.info(f'Weather in {location},{region} at {time}: {temperature}')