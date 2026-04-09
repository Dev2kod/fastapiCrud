import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

CLIP_DURATION = 4 * 60  # 4 minutes
BASE_URL = "http://172.16.23.81/rtsp_clips/"


# eg: "2024-06-01 12:34:56" → find clip → extract ±5 sec
#what it does : 1. Takes a timestamp as input.
#2. Calls find_clip to determine which video clip contains that timestamp and calculates the offset.
#3. If a clip is found, it constructs the video URL and uses FFmpeg to extract a 10-second segment around the timestamp (±5 seconds).
#4. The extracted clip is saved to the output directory with a unique filename.
#5. If no clip is found or if FFmpeg encounters an error, it prints an appropriate message and returns None.
#6. Finally, it returns the path to the created clip if successful.
def get_video_list():
    """
    Fetch list of videos from NGINX directory
    """
    try:
        print("Fetching video list from NGINX...")
        response = requests.get(BASE_URL)
        if response.status_code != 200:
            print("Failed to fetch video list")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        files = []
        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.endswith(".mp4"):
                files.append(href)

        return files

    except Exception as e:
        print("Error fetching video list:", str(e))
        return []

# Convert filename → datetime
# clip_20260330_102000.mp4 → datetime
#eg : "clip_20260330_102000.mp4" → datetime object representing 2024-06-30 10:20:00
def parse_filename(filename):
    """
    Convert filename → datetime
    clip_20260330_102000.mp4 → datetime
    """
    try:
        print(f"Parsing filename: {filename}")
        name = filename.replace("clip_", "").replace(".mp4", "")
        return datetime.strptime(name, "%Y%m%d_%H%M%S")
    except:
        print(f"Error parsing filename: {filename}")
        return None


def find_clip(input_timestamp):
    """
    Find which clip contains the timestamp
    """
    try:
        print(f"Finding clip for timestamp: {input_timestamp}")
        input_time = datetime.strptime(input_timestamp, "%Y-%m-%d %H:%M:%S")
    except:
        print("Invalid timestamp format")
        return None, None

    files = get_video_list()

    # 🔥 CRITICAL FIX: sort files
    files.sort(key=lambda x: parse_filename(x) or datetime.min)

    for file in files:
        start_time = parse_filename(file)
        if not start_time:
            continue

        end_time = start_time + timedelta(seconds=CLIP_DURATION)

        print(f"Checking: {file} | Range: {start_time} → {end_time}")

        if start_time <= input_time < end_time:
            offset = (input_time - start_time).seconds
            print(f"✅ Selected: {file}, Offset: {offset}")
            return file, offset

    print("❌ No matching clip found")
    return None, None