import time
import logging
import uvicorn
from datetime import datetime
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, Response, JSONResponse

from utils import generate_css_bar, SongDetailFetcher


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Item(BaseModel):
    url: str

app = FastAPI(title="PastFm Backend", description="Welcome to PastFm's Backend", version="1.0")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def display() -> RedirectResponse:
    return RedirectResponse(url="https://github.com/arpy8/PastFm")

@app.get("/live")
async def live_banner(request: Request, user="arpy8", color="f70000") -> RedirectResponse:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return RedirectResponse(url=f"/render?user={user}&color={color}&t={timestamp}")

@app.get("/render")
async def spotify_banner(request: Request, user: str = "arpy8", color: str = "f70000", t: str = None) -> Response:
    try:
        num_bar = 75
        css_bar = generate_css_bar(num_bar)

        song_details = SongDetailFetcher(user=user)
        result = song_details.get_details()

        if not result:
            return JSONResponse(
                content={"success": False, "message": "Failed to fetch song details"},
                status_code=404,
            )
        
        timestamp = t or datetime.now().strftime("%Y%m%d%H%M%S")
        color = color or "f70000"
        
        context = {
            "title_text": "Now playing" if result["is_playing"] else "Last played",
            "color": color,
            "song_name": result["song"],
            "artist_name": result["artist"],
            "thumbnail": result["thumbnail"],
            "url": result["url"],
            "css_bar": css_bar,
            "timestamp": timestamp,
            "cover_image": True,
            "content_bar": "".join(["<div class='bar'></div>" for i in range(num_bar)]),
        }

        svg_content = templates.get_template("default_theme.html").render(context)

        headers = {
            "Cache-Control": "private, no-cache, no-store, must-revalidate, max-age=0",
            "Pragma": "no-cache",
            "Expires": "-1",
            "ETag": f'W/"{timestamp}"',
            "Last-Modified": datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        }

        return Response(
            content=svg_content, media_type="image/svg+xml", headers=headers
        )
    except Exception as e:
        logger.error(f"Error rendering banner: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error rendering banner: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=7860, reload=True)