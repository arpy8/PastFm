import random
import base64
import logging
import requests
import urllib.parse
from PIL import Image
import os, requests, shutil
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
    def __init__(self):
        self.out_dir = "out"
        self.crop_val=(105, 45, 375, 315)
        self.thumbnail_url = "https://img.youtube.com/vi/{}/0.jpg"
        self.yt_api_key = os.getenv("YT_API_KEY")
        
        os.makedirs(self.out_dir, exist_ok=True)
    
    def extract_video_id(self, url):
        parsed = urllib.parse.parse_qs(url)
        return list(parsed.values())[0][0]

    def get_details(self, video_url):
        logger.info(f"Fetching details for URL: {video_url}")
        
        song_info = self.get_song_info(video_url)
        if "error" in song_info:
            logger.error(f"Error fetching song info: {song_info['error']}")
            return None
        
        thumbnail = self.get_thumbnail(video_url)
        if not thumbnail:
            logger.error("Error fetching thumbnail")
            return None
        
        song_info["thumbnail"] = thumbnail.decode("utf-8")
        song_info["url"] = video_url
        
        return song_info
        
    def get_song_info(self, video_url):
        video_id = self.extract_video_id(video_url)
        
        if not video_id:
            return {"error": "Invalid YouTube URL or video ID"}
        
        try:
            youtube = build('youtube', 'v3', developerKey=self.yt_api_key)
            video_response = youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                return {"error": "Video not found"}
            
            video_info = video_response['items'][0]['snippet']
            
            return {
                "song": video_info['title'],
                "artist": video_info['channelTitle'].replace(" - Topic", "").strip(),
            }
            
        except HttpError as e:
            return {"error": f"API Error: {e.reason}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}

    def get_thumbnail(self, video_url):
        video_id = self.extract_video_id(video_url)
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