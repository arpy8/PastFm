import random
import base64
import requests
import urllib.parse
from PIL import Image
import os, requests, shutil
from bs4 import BeautifulSoup
import logging

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
    def __init__(self):
        self.out_dir = "out"
        self.crop_val=(105, 45, 375, 315)
        self.thumbnail_url = "https://img.youtube.com/vi/{}/0.jpg"
        
        os.makedirs(self.out_dir, exist_ok=True)
    
    def find_video_id(self, url):
        parsed = urllib.parse.parse_qs(url)
        return list(parsed.values())[0][0]

    def get_artist_name(self, soup):
        meta_tags = soup.find_all("meta")
        try:
            return [meta for meta in meta_tags if meta.has_attr('property') and meta['property'] == 'og:video:tag'][0].get('content')
        except Exception as e:
            print(f"Error finding artist name: {e}")
            return "Youtube Music"
        
    def get_details(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            titles = soup.find_all("title")
            
            details = str(titles[1]).strip("<title></").split(" - ")
            if "Youtube Music" in details and len(details) > 2:
                details.remove("Youtube Music")
            
            song = details[1] if len(details) > 1 else details[0]
            song = song.replace("(Official Video)", "").replace("(Official Audio)", "").strip()
            
            artist = self.get_artist_name(soup)
            thumbnail = self.fetch_thumbnail(url)
            print({"url":url, "song": song, "artist": artist})

            return {"song": song, "artist": artist, "url":url, "thumbnail": thumbnail}

        except requests.exceptions.RequestException as e:
            print(f"Error fetching details for {url}: {e}")
            return False

    def fetch_thumbnail(self, video_url):
        video_id = self.find_video_id(video_url)
        url = self.thumbnail_url.format(video_id)
        logger.info(f"Fetching thumbnail for video ID: {video_id}")
        
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open("temp.png", "wb") as file:
                shutil.copyfileobj(response.raw, file)
            
            with Image.open("temp.png") as im:
                cropped_im = im.crop(self.crop_val)
                output_path = os.path.join(self.out_dir, f"temp.png")
                cropped_im.save(output_path, quality=95)
            
            os.remove("temp.png")
            
            try:
                with open("out/temp.png", "rb") as image_file:
                    image_data = image_file.read()
                    logger.info(f"Successfully read thumbnail of size: {len(image_data)} bytes")
                    return base64.b64encode(image_data)
            except Exception as e:
                logger.error(f"Error reading processed thumbnail: {e}", exc_info=True)
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading thumbnail: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Error processing thumbnail: {e}", exc_info=True)
            return None

if __name__=="__main__":
    url = [
        "https://music.youtube.com/watch?v=1P4UaohygEg&list=RDAMVM1afGL2Y1HuM"
        "https://music.youtube.com/watch?v=Ya21jMaTkK0&list=RDAMVM1afGL2Y1HuM",
        "https://music.youtube.com/watch?v=3rfo5cq-uAk&list=RDAMVM1afGL2Y1HuM",
        "https://music.youtube.com/watch?v=YWpI5jOetrY&list=RDAMVM1afGL2Y1HuM",
        "https://music.youtube.com/watch?v=Il4o_jJMq10&list=RDAMVM1afGL2Y1HuM",
        "https://music.youtube.com/watch?v=OgiVdIob-YI&list=RDAMVM1afGL2Y1HuM"
        
    ]

    a = SongDetailFetcher()
    for i in url:
        result = a.get_details(i)