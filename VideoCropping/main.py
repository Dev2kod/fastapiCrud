from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from services.videoService import process_timestamp
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS (needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TimestampRequest(BaseModel):
    timestamp: str


@app.post("/clip")
def get_clip(request: TimestampRequest):
    print(f"Received request for clip: {request.timestamp}")
    output_file = process_timestamp(request.timestamp)

    if not output_file or not os.path.exists(output_file):
        raise HTTPException(status_code=404, detail="No clip found")

    print(f"Returning clip: {output_file}")
    return FileResponse(
        output_file,
        media_type="video/mp4",
        filename="clip.mp4"
    )