import aiohttp
import asyncio
import backoff


class AsyncPexelsClient:
    """
    Asynchronous Python client for the Pexels API.

    The Pexels API provides programmatic access to the Pexels library of photos and videos.
    This client supports asynchronous operations for searching photos and videos, getting
    details of a specific photo or video, getting curated and popular photos, and downloading
    a specific photo or video.

    Rate Limits:
    By default, the Pexels API is rate-limited to 200 requests per hour and 20,000 requests per month.
    If you need a higher limit, you may contact Pexels to request it.

    Usage:
    ```python
    client = AsyncPexelsClient("your_api_key")
    photos = await client.search_photos("cats")
    ```

    Note: Replace "your_api_key" with your actual Pexels API key.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/v1"

    @backoff.on_exception(backoff.expo,
                          (aiohttp.ClientError, asyncio.TimeoutError),
                          max_tries=8)
    async def _make_request(self, endpoint, params=None):
        headers = {"Authorization": self.api_key}
        params = {k: v for k, v in params.items() if v is not None}  # remove None values
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/{endpoint}", headers=headers, params=params) as response:
                response.raise_for_status()
                return await response.json()

    async def search_photos(self, query, per_page=15, page=1, orientation=None, size=None, locale=None):
        """
        Search for photos by query.
        Maximum items per page: 80
        
        Additional Arguments:
        orientation (string - optional):    Desired photo or video orientation. 
                                            The current supported orientations are: "landscape", "portrait" or "square".

        size (string - optional):           Minimum photo or video size. 
                                            The current supported sizes are: large (24MP), medium (12MP) or small (4MP).

        locale (string - optional):         The locale of the search you are performing. 
        The current supported locales are:  "en-US", "pt-BR", "es-ES", "ca-ES", "de-DE", "it-IT", "fr-FR", "sv-SE", "id-ID", "pl-PL", 
                                            "ja-JP", "zh-TW", "zh-CN", "ko-KR", "th-TH", "nl-NL", "hu-HU", "vi-VN", "cs-CZ", "da-DK", 
                                            "fi-FI", "uk-UA", "el-GR", "ro-RO", "nb-NO", "sk-SK", "tr-TR", 'ru-RU".
        """
        endpoint = "search"
        params = {"query": query, "per_page": per_page, "page": page, "orientation": orientation, "size": size, "locale": locale}
        return await self._make_request(endpoint, params)

    async def search_videos(self, query, per_page=15, page=1, orientation=None, size=None, locale=None):
        """
        Search for videos by query.
        Maximum items per page: 80
                
        Additional Arguments:
        orientation (string - optional):    Desired photo or video orientation. 
                                            The current supported orientations are: "landscape", "portrait" or "square".

        size (string - optional):           Minimum photo or video size. 
                                            The current supported sizes are: large (24MP), medium (12MP) or small (4MP).

        locale (string - optional):         The locale of the search you are performing. 
        The current supported locales are:  "en-US", "pt-BR", "es-ES", "ca-ES", "de-DE", "it-IT", "fr-FR", "sv-SE", "id-ID", "pl-PL", 
                                            "ja-JP", "zh-TW", "zh-CN", "ko-KR", "th-TH", "nl-NL", "hu-HU", "vi-VN", "cs-CZ", "da-DK", 
                                            "fi-FI", "uk-UA", "el-GR", "ro-RO", "nb-NO", "sk-SK", "tr-TR", 'ru-RU".
        """
        endpoint = "videos/search"
        params = {"query": query, "per_page": per_page, "page": page, "orientation": orientation, "size": size, "locale": locale}
        return await self._make_request(endpoint, params)

    async def get_photo(self, photo_id):
        """
        Get details of a specific photo by its ID.
        """
        endpoint = f"photos/{photo_id}"
        return await self._make_request(endpoint)

    async def get_video(self, video_id):
        """
        Get details of a specific video by its ID.
        """
        endpoint = f"videos/videos/{video_id}"
        return await self._make_request(endpoint)

    async def get_curated_photos(self, per_page=15, page=1):
        """
        Get curated photos.
        Maximum items per page: 80
        """
        endpoint = "curated"
        params = {"per_page": per_page, "page": page}
        return await self._make_request(endpoint, params)

    async def get_popular_photos(self, per_page=15, page=1):
        """
        Get popular photos.
        Maximum items per page: 80
        """
        endpoint = "popular"
        params = {"per_page": per_page, "page": page}
        return await self._make_request(endpoint, params)

    async def download_photo(self, photo_id):
        """
        Download a specific photo by its ID.
        """
        photo_data = await self.get_photo(photo_id)
        photo_url = photo_data["src"]["original"]
        async with aiohttp.ClientSession() as session:
            async with session.get(photo_url) as response:
                response.raise_for_status()
                return await response.read()

    async def download_video(self, video_id):
        """
        Download a specific video by its ID.
        """
        video_data = await self.get_video(video_id)
        video_url = video_data["video_files"][0]["link"]
        async with aiohttp.ClientSession() as session:
            async with session.get(video_url) as response:
                response.raise_for_status()
                return await response.read()