import os
import json
import base64
import random
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def generate_css_bar(num_bar=75):
    css_bar = ""
    left = 1
    for i in range(1, num_bar + 1):
        anim = random.randint(350, 500)
        css_bar += (
            ".bar:nth-child({})  {{ left: {}px; animation-duration: {}ms; }}".format(
                i, left, anim
            )
        )
        left += 4

    return css_bar

class SongDetailFetcher:
    def __init__(self, user="arpy8"):
        self.user = user
        self.lastfm_api_key = os.getenv("LASTFM_API_KEY")
        self.no_scrobble_url = f"https://ws.audioscrobbler.com/2.0/?api_key={self.lastfm_api_key}&method=User.getrecenttracks&user={self.user}&format=json&limit=1"
        self.scrobble_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks&user={self.user}&limit=1&extended=1&api_key={self.lastfm_api_key}&format=json"
        # self.no_scrobble_url = f"https://ws.audioscrobbler.com/2.0/?api_key={self.lastfm_api_key}&method=User.getrecenttracks&user={self.user}&format=json&limit=1"

    def get_base64_image(self, url):
        try:
            if url == "":
                with open("./static/temp.gif", "rb") as image_file:
                    image_data = image_file.read()
                    return base64.b64encode(image_data).decode('utf-8')
                
            response = requests.get(url)
            response.raise_for_status()
            
            base64_image = base64.b64encode(response.content).decode('utf-8')
            return base64_image
        except requests.exceptions.RequestException as e:
            print(f"Error fetching image: {e}")
            return None

    def get_details(self):
        try:
            scrobble_rslt = requests.get(self.scrobble_url)
            no_scrobble_rslt = requests.get(self.no_scrobble_url)
            
            scrobble_rslt = json.loads(scrobble_rslt.text)['recenttracks']["track"][0]
            no_scrobble_rslt = json.loads(no_scrobble_rslt.text)['recenttracks']["track"][0]

            artist = no_scrobble_rslt["artist"]["#text"]
            name = no_scrobble_rslt["name"]
            is_playing = "@attr" in no_scrobble_rslt
            url = no_scrobble_rslt["url"]
            
            thumbnail = self.get_base64_image(scrobble_rslt["image"][-1]["#text"])
                
            return {
                "song": name,
                "artist": artist,
                "thumbnail": thumbnail,
                "url": url,
                "is_playing": is_playing,
            }

        except Exception as e:
            logger.error(f"Error fetching song details: {e}")
            return None