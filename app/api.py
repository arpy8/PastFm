"""FastAPI application for the PastFm service."""

from typing import Optional
from datetime import datetime
from xml.sax.saxutils import escape

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, Response, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config import config, BASE_DIR
from utils import generate_css_bar, generate_bar_elements, LastFmClient, logger


class Item(BaseModel):
    """Pydantic model for URL input."""

    url: str


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI instance
    """
    app = FastAPI(
        title="PastFm API",
        description="LastFM scrobble card generator for GitHub profile README",
        version="1.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

    @app.get("/")
    async def root() -> RedirectResponse:
        """Redirect to project GitHub page."""
        return RedirectResponse(url="https://github.com/arpy8/PastFm")

    @app.get("/redirect")
    async def redirect() -> RedirectResponse:
        """Redirect to project repository."""
        return RedirectResponse(url="https://github.com/arpy8/PastFm")

    @app.get("/live")
    async def live_banner(
        request: Request,
        user: str = config.default_user,
        color: str = config.default_color,
    ) -> RedirectResponse:
        """
        Generate a timestamped redirect to ensure fresh content.

        Args:
            request: FastAPI request object
            user: LastFM username
            color: Hex color code (without #)

        Returns:
            Redirect to the render endpoint with timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return RedirectResponse(url=f"/render?user={user}&color={color}&t={timestamp}")

    @app.get("/render")
    async def render_banner(
        request: Request,
        user: str = config.default_user,
        color: str = config.default_color,
        t: Optional[str] = None,
    ) -> Response:
        """
        Render the LastFM now playing/recently played card.

        Args:
            request: FastAPI request object
            user: LastFM username
            color: Hex color code (without #)
            t: Timestamp for cache busting

        Returns:
            SVG image response

        Raises:
            HTTPException: If rendering fails
        """
        try:
            css_bar = generate_css_bar(config.num_bars)

            lastfm_client = LastFmClient(username=user)
            result = lastfm_client.get_current_track()

            if not result:
                return JSONResponse(
                    content={
                        "success": False,
                        "message": "Failed to fetch song details",
                    },
                    status_code=404,
                )

            timestamp = t or datetime.now().strftime("%Y%m%d%H%M%S")
            context = {
                "title_text": "Now playing" if result["is_playing"] else "Last played",
                "color": color,
                "song_name": escape(result["song"]),
                "artist_name": escape(result["artist"]),
                "thumbnail": result["thumbnail"],
                "url": escape(result["url"]) if result["url"] else "",
                "css_bar": css_bar,
                "timestamp": timestamp,
                "cover_image": bool(result["thumbnail"]),
                "content_bar": generate_bar_elements(config.num_bars),
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
            logger.error(f"Error rendering banner: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error rendering banner: {str(e)}"
            )

    @app.get("/health")
    async def health_check() -> JSONResponse:
        """Check application health status."""
        return JSONResponse(
            content={"status": "healthy", "version": app.version}, status_code=200
        )

    return app


def start_server() -> None:
    """Start the uvicorn server for local development."""
    uvicorn.run("pastfm.app:app", host="0.0.0.0", port=7860, reload=config.debug)
