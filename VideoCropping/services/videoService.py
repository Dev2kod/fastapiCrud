import datetime
import subprocess
import os
import uuid
from services.clipFinder import find_clip

FFMPEG_PATH = os.path.join(os.getcwd(), "ffmpeg", "bin", "ffmpeg.exe")
VIDEO_BASE_URL = "http://172.16.23.81/rtsp_clips"

# example timestamp: "2024-06-01T12:34:56Z"
# output: clip from 12:34:51 to 12:35:01 (±5 sec around the timestamp)
def process_timestamp(input_timestamp):
    """
    timestamp → find clip → extract ±5 sec
    """
    print(f"Processing timestamp from video service: {input_timestamp}")
    
    video_name, offset = find_clip(input_timestamp)

    if not video_name:  
        print("No video found")
        return None

    video_url = f"{VIDEO_BASE_URL}/{video_name}"

    start_time = max(0, offset - 5)
    duration = 10

    output_file = os.path.join("output", f"{uuid.uuid4()}.mp4")

    command = [
        FFMPEG_PATH,
        "-i", video_url,              # 🔥 FIX: input first
        "-ss", str(start_time),       # accurate seek
        "-t", str(duration),
        "-c:v", "libx264",
        "-c:a", "aac",
        "-movflags", "+faststart",
        output_file
    ]

    print(f"\n🚀 Running FFmpeg: {datetime.datetime.now()}")
    
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"FFmpeg finished with return code {result.returncode}")
    if result.returncode != 0:
        print("❌ FFmpeg Error:\n", result.stderr)
        return None

    print(f"✅ Clip created: {datetime.datetime.now()} - {output_file}")
    return output_file