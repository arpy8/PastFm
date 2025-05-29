"""Configuration settings for PastFm application."""

import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

BASE_DIR = Path(__file__).parent


class LastFmConfig(BaseModel):
    """LastFM API configuration."""

    api_key: str = Field(
        default_factory=lambda: os.getenv("LASTFM_API_KEY", ""),
        description="LastFM API key",
    )
    base_url: str = "https://ws.audioscrobbler.com/2.0/"


class AppConfig(BaseModel):
    """Application configuration."""

    lastfm: LastFmConfig = LastFmConfig()
    default_user: str = "arpy8"
    default_color: str = "f70000"
    num_bars: int = 75
    debug: bool = bool(os.getenv("DEBUG", "False").lower() == "true")


config = AppConfig()
