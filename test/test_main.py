"""Unit tests for the weather script in the main module."""
import unittest
from unittest.mock import patch, Mock
import os
import sys
import requests
from bs4 import BeautifulSoup
sys.path.append("src")
from main import setup_logger, get_api_key #pylint: disable=wrong-import-position,import-error

class TestWeatherScript(unittest.TestCase):
    """Test cases for the weather script functions."""

    @patch("logging.getLogger")
    def test_setup_logger(self, mock_get_logger):
        """Test if logger is set up correctly."""
        mock_logger = Mock()
        mock_get_logger.return_value = mock_logger
        file_name = "test_status.log"
        logger = setup_logger(file_name)
        self.assertTrue(os.path.isfile(file_name))
        self.assertEqual(logger, mock_logger)

    @patch.dict(os.environ, {"WEATHER_API_KEY": "test_key"})
    def test_api_key_set(self):
        """Test if API key is correctly set from environment variables."""
        logger = Mock()
        api_key = get_api_key(logger)
        self.assertEqual(api_key, "test_key")

    def test_api_endpoint_reachability(self):
        """Test if the weather API endpoint is reachable."""
        try:
            response = requests.get("http://api.weatherapi.com/", timeout=10)
            html = response.content.decode("utf-8").strip()
            soup = BeautifulSoup(html, "html.parser")
            message = soup.text.replace("\ufeff", "").strip()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(message, "All OK")
        except requests.RequestException as e:
            self.fail(f"API request failed with exception: {e}")


if __name__ == "__main__":
    unittest.main()
