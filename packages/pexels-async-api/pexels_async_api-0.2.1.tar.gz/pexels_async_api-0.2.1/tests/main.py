# TODO: Write tests for the AsyncPexelsClient class

import unittest
from pexels_async_api.client import AsyncPexelsClient

class TestAsyncPexelsClient(unittest.TestCase):
    def setUp(self):
        self.client = AsyncPexelsClient("your_api_key")  # replace "your_api_key" with your actual Pexels API key

    def test_search_photos(self):
        pass

    def test_search_videos(self):
        pass


if __name__ == "__main__":
    unittest.main()
