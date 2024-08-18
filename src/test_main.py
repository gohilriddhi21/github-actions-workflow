import unittest
import os
import requests
from bs4 import BeautifulSoup
from unittest.mock import patch, Mock
from main import setup_logger, get_api_key


class TestWeatherScript(unittest.TestCase):

    def test_setup_logger(self):
        """Test if logger is set up correctly."""
        file_name = "test_status.log"
        logger = setup_logger(file_name)
        self.assertTrue(os.path.isfile(file_name))

    @patch.dict(os.environ, {"WEATHER_API_KEY": "test_key"})
    def test_api_key_set(self):
        """Test if API key is correctly set from environment variables."""
        logger = Mock()
        api_key = get_api_key(logger)
        self.assertEqual(api_key, "test_key")

    def test_api_endpoint_reachability(self):
        """Test if the weather API endpoint is reachable."""
        try:
            response = requests.get("http://api.weatherapi.com/")
            html = response.content.decode("utf-8").strip()
            soup = BeautifulSoup(html, "html.parser")
            message = soup.text.replace("\ufeff", "").strip()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(message, "All OK")
        except requests.RequestException as e:
            self.fail(f"API request failed with exception: {e}")


if __name__ == "__main__":
    unittest.main()
