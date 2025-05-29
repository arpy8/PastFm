"""PastFm main application entry point."""

import uvicorn
from app.api import create_app
from config import config

app = create_app()

if __name__ == "__main__":
    print("Starting PastFm application")
    uvicorn.run(
        "main:app", host="0.0.0.0", port=7860, reload=config.debug, log_level="info"
    )
