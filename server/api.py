import json
import logging
import uvicorn

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils import generate_css_bar, SongDetailFetcher
from db import get_data, update_local_db, update_remote_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Item(BaseModel):
    url: str

app = FastAPI(title="PastFm Backend", description="Welcome to PastFm's Backend", version="1.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "chrome-extension://*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def display() -> RedirectResponse:
    return RedirectResponse(url="https://github.com/arpy8/PastFm")

@app.post("/update")
async def update_data(item: Item) -> JSONResponse:
    if item.url.lower() == "nan":
        return JSONResponse(
            content={"success": False, "message": "Invalid URL provided"},
            status_code=400
        )
    
    try:
        song_details = SongDetailFetcher()
        result = song_details.get_details(item.url)
        logger.info(f"Fetched details: {result}")
        
        if not result:
            return JSONResponse(
                content={"success": False, "message": "Failed to fetch song details"},
                status_code=404
            )
        
        local_success, local_message = update_local_db(result)
        remote_success, remote_message = update_remote_db(result)
        
        if local_success and remote_success:
            return JSONResponse(
                content={"success": True, "message": "Data updated successfully!"},
                status_code=200
            )
        else:
            return JSONResponse(
                content={
                    "success": False,
                    "message": f"Database update failed: {local_message if not local_success else ''}{remote_message if not remote_success else ''}"
                },
                status_code=500
            )
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JSONResponse(
            content={"success": False, "message": f"Error: {str(e)}"},
            status_code=500
        )

@app.get("/render")
async def spotify_banner(request: Request) -> Response:
    try:
        num_bar = 75
        css_bar = generate_css_bar(num_bar)

        data = get_data()
        if not data:
            raise HTTPException(status_code=404, detail="No data available")
            
        time, song, artist, url, thumbnail = data[-1]
        logger.info(f"Rendering banner for: {time}, {song}, {artist}, {url}")
        
        context = {
            "height": "435",
            "background_color": "#000000",
            "bar_color": "#ff0000",
            "title_text": "Now playing",
            "song_name": song,
            "artist_name": artist,
            "content_bar": "".join(["<div class='bar'></div>" for i in range(num_bar)]),
            "thumbnail": thumbnail.decode("utf-8"),
            "cover_image": True,
            "css_bar": css_bar,
            "url": url
        }
        
        svg_content = templates.get_template("default_theme.html").render(context)
        
        return Response(
            content=svg_content,
            media_type="image/svg+xml"
        )
    except Exception as e:
        logger.error(f"Error rendering banner: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error rendering banner: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)