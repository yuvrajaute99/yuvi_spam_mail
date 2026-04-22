"""
FastAPI backend for the Email/SMS Spam Detection system.

Endpoints
---------
GET  /              – serve web UI
GET  /health        – health-check
POST /predict       – classify a text as spam or ham

Usage:
    uvicorn api:app --host 0.0.0.0 --port 8000
    Then visit: http://localhost:8000/
"""

import logging
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from predict import predict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Email Spam Detection API",
    description="Classify email / SMS text as spam or ham.",
    version="1.0.0",
)

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static files if directory exists
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ---------------------------------------------------------------------------
# DTOs
# ---------------------------------------------------------------------------

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Email / SMS body text")


class PredictResponse(BaseModel):
    label: str
    confidence: float


class HealthResponse(BaseModel):
    status: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
async def serve_ui():
    """Serve the web UI (index.html)."""
    index_path = os.path.join(TEMPLATES_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="UI not found")
    return FileResponse(index_path, media_type="text/html")


@app.get("/health", response_model=HealthResponse)
async def health():
    """Simple health-check."""
    return HealthResponse(status="ok")


@app.post("/predict", response_model=PredictResponse)
async def predict_endpoint(request: PredictRequest):
    """Classify input text as spam or ham."""
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text must not be empty.")

    try:
        result = predict(text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        logger.exception("Unexpected error during prediction")
        raise HTTPException(status_code=500, detail="Internal server error")

    return PredictResponse(**result)
