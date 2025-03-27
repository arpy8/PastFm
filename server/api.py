import os
import atexit
import numpy as np
import json, requests
from PIL import Image
import tensorflow as tf
from pathlib import Path
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from database import update_data_field, cleanup
from fastapi import FastAPI, UploadFile, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from constants import example_data


DRISHTI_AUTH_KEY = os.environ.get("DRISHTI_AUTH_KEY")
DRISHTI_AUTH_KEY_NAME = os.environ.get("DRISHTI_AUTH_KEY_NAME")

if not DRISHTI_AUTH_KEY:
    raise ValueError("DRISHTI_AUTH_KEY environment variable must be set")

class Item(BaseModel):
    uuid: str
    time: str
    humidity: str
    temperature: str
    soil_moisture: str


api_key_header = APIKeyHeader(name=DRISHTI_AUTH_KEY_NAME, auto_error=True)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != DRISHTI_AUTH_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key",
        )
    return api_key

mongo_string = os.environ.get("MONGO_STRING")
app = FastAPI(title="Dristhi Backend", description="APIs for Dristhi", version="1.0")

def load_model():
    model_path = (
        Path(__file__).resolve().parent.parent
        / "weights"
        / "plant_disease_classifier.h5"
    )
    model = tf.keras.models.load_model(model_path)
    return model

@app.get("/")
async def display() -> str:
    # response = RedirectResponse(url='https://github.com/epicshi')
    return "Welcome to Dristhi Backend"

@app.post("/predict")
async def predict(
    file: UploadFile,
    api_key: str = Depends(verify_api_key)
) -> str:
    model = load_model()

    original_image = Image.open(file.file).convert("RGB")
    preprocessed_image = original_image.resize((256, 256))
    preprocessed_image = np.array(preprocessed_image)[:, :, :3] / 255.0
    preds = model.predict(np.expand_dims(preprocessed_image, axis=0))

    labels = ["Healthy", "Powdery", "Rust"]
    preds_class = np.argmax(preds)
    preds_label = labels[preds_class]

    return preds_label

@app.post("/update-data")
async def update_data(
    item: Item,
    api_key: str = Depends(verify_api_key)
) -> str:
    if (
        item.humidity.lower() == "nan"
        or item.temperature.lower() == "nan"
        or item.soil_moisture.lower() == "nan"
    ):
        return "Invalid data"

    return update_data_field(
        str(item.uuid),
        {
            "timestamp": int(item.time),
            "humidity": float(item.humidity),
            "temperature": float(item.temperature),
            "soil_moisture": float(item.soil_moisture),
        },
    )

@app.get("/fetch-news")
async def fetch_news(
    api_key: str = Depends(verify_api_key)
):
    news_api_key = os.environ.get("NEWS_API_KEY")
    if not news_api_key:
        raise HTTPException(
            status_code=500,
            detail="News API key not configured"
        )
    
    response = requests.get(
        'https://newsapi.org/v2/everything',
        params={
            'q': '(farmer OR agriculture OR "rural development" OR "farm laws" OR kisaan OR kisan) AND (India OR Maharashtra OR Punjab OR Karnataka OR "Uttar Pradesh")',
            'language': 'en',
            'sortBy': 'publishedAt',
            'apiKey': news_api_key
        }
    )
    if response.status_code != 200:
        # print(response.content)
        # raise HTTPException(
        #     status_code=500,
        #     detail="News API request failed"
        # )
        return example_data
    
    return json.loads(response.content)


@app.get("/last-data")
async def last_data(    
    api_key: str = Depends(verify_api_key)
):
    return "returns last 10 data"


if __name__ == "__main__":
    import uvicorn
    try:
        uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)
    finally:
        cleanup()
        atexit.register(cleanup)