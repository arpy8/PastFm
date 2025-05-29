"""LastFM API client for fetching user's recently played tracks."""

import json
import base64
import requests
from typing import Dict, Optional, Any

from config import config
from utils.logging_config import logger


class LastFmClient:
    """Client for interacting with LastFM API."""

    def __init__(self, username: str = config.default_user) -> None:
        """
        Initialize LastFM client for a specific user.

        Args:
            username: LastFM username to fetch data for
        """
        self.username = username
        self.api_key = config.lastfm.api_key
        self.base_url = config.lastfm.base_url

    def _build_url(self, method: str, extended: bool = False) -> str:
        """
        Build a LastFM API URL.

        Args:
            method: LastFM API method name
            extended: Whether to request extended track info

        Returns:
            Fully qualified URL for the API request
        """
        params = {
            "method": method,
            "user": self.username,
            "api_key": self.api_key,
            "format": "json",
            "limit": 1,
        }

        if extended:
            params["extended"] = 1

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.base_url}?{query_string}"

    @staticmethod
    def get_base64_image(url: str) -> Optional[str]:
        """
        Convert an image URL to base64 encoding.

        Args:
            url: URL of the image to convert

        Returns:
            Base64-encoded image string or None if failed
        """
        try:
            if not url:
                with open("./static/temp.gif", "rb") as image_file:
                    image_data = image_file.read()
                    return base64.b64encode(image_data).decode("utf-8")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return base64.b64encode(response.content).decode("utf-8")
        except Exception as e:
            logger.error(f"Error fetching image: {e}")
            return None

    def get_current_track(self) -> Optional[Dict[str, Any]]:
        """
        Fetch user's current or last played track from LastFM.

        Returns:
            Dictionary with track details or None if failed
        """
        try:
            scrobble_url = self._build_url("user.getRecentTracks", extended=True)

            status_url = self._build_url("User.getrecenttracks")

            scrobble_response = requests.get(scrobble_url, timeout=10)
            status_response = requests.get(status_url, timeout=10)

            scrobble_data = json.loads(scrobble_response.text)["recenttracks"]["track"][
                0
            ]
            status_data = json.loads(status_response.text)["recenttracks"]["track"][0]

            artist = status_data["artist"]["#text"]
            name = status_data["name"]
            is_playing = "@attr" in status_data
            track_url = status_data["url"]

            image_url = scrobble_data.get("image", [])[-1].get("#text", "")
            thumbnail = self.get_base64_image(image_url)

            return {
                "song": name,
                "artist": artist,
                "thumbnail": thumbnail,
                "url": track_url,
                "is_playing": is_playing,
            }

        except Exception as e:
            logger.error(f"Error fetching song details: {e}")
            return None