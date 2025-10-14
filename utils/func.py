# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import concurrent.futures
import time
import os
import re
import cv2
import logging
import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB as MONGO_URI, DB_NAME

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

PUBLIC_LINK_PATTERN = re.compile(r'(https?://)?(t\.me|telegram\.me)/([^/]+)(/(\d+))?')
PRIVATE_LINK_PATTERN = re.compile(r'(https?://)?(t\.me|telegram\.me)/c/(\d+)(/(\d+))?')
VIDEO_EXTENSIONS = {"mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "mpeg", "mpg", "3gp"}

mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client[DB_NAME]
users_collection = db["users"]
premium_users_collection = db["premium_users"]
statistics_collection = db["statistics"]
codedb = db["redeem_code"]

# ------- < start > Session Encoder don't change -------

a1 = "c2F2ZV9yZXN0cmljdGVkX2NvbnRlbnRfYm90cw=="
a2 = "Nzk2"
a3 = "Z2V0X21lc3NhZ2Vz" 
a4 = "cmVwbHlfcGhvdG8=" 
a5 = "c3RhcnQ="
attr1 = "cGhvdG8="
attr2 = "ZmlsZV9pZA=="
a7 = "SGkg8J+RiyBXZWxjb21lLCBXYW5uYSBpbnRyby4uLj8gCgrinLPvuI8gSSBjYW4gc2F2ZSBwb3N0cyBmcm9tIGNoYW5uZWxzIG9yIGdyb3VwcyB3aGVyZSBmb3J3YXJkaW5nIGlzIG9mZi4gSSBjYW4gZG93bmxvYWQgdmlkZW9zL2F1ZGlvIGZyb20gWVQsIElOU1RBLCAuLi4gc29jaWFsIHBsYXRmb3JtcwrinLPvuI8gU2ltcGx5IHNlbmQgdGhlIHBvc3QgbGluayBvZiBhIHB1YmxpYyBjaGFubmVsLiBGb3IgcHJpdmF0ZSBjaGFubmVscywgZG8gL2xvZ2luLiBTZW5kIC9oZWxwIHRvIGtub3cgbW9yZS4="
a8 = "Sm9pbiBDaGFubmVs"
a9 = "R2V0IFByZW1pdW0=" 
a10 = "aHR0cHM6Ly90Lm1lL3RlYW1fc3B5X3Bybw==" 
a11 = "aHR0cHM6Ly90Lm1lL2tpbmdvZnBhdGFs" 

# ------- < end > Session Encoder don't change --------

def is_private_link(link):
    return bool(PRIVATE_LINK_PATTERN.match(link))


def thumbnail(sender):
    return f'{sender}.jpg' if os.path.exists(f'{sender}.jpg') else None


def hhmmss(seconds):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))


def E(L):   
    private_match = re.match(r'https://t\.me/c/(\d+)/(?:\d+/)?(\d+)', L)
    public_match = re.match(r'https://t\.me/([^/]+)/(?:\d+/)?(\d+)', L)
    
    if private_match:
        return f'-100{private_match.group(1)}', int(private_match.group(2)), 'private'
    elif public_match:
        return public_match.group(1), int(public_match.group(2)), 'public'
    
    return None, None, None


def get_display_name(user):
    if user.first_name and user.last_name:
        return f"{user.first_name} {user.last_name}"
    elif user.first_name:
        return user.first_name
    elif user.last_name:
        return user.last_name
    elif user.username:
        return user.username
    else:
        return "Unknown User"


def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)


def get_dummy_filename(info):
    file_type = info.get("type", "file")
    extension = {
        "video": "mp4",
        "photo": "jpg",
        "document": "pdf",
        "audio": "mp3"
    }.get(file_type, "bin")
    
    return f"downloaded_file_{int(time.time())}.{extension}"


async def is_private_chat(event):
    return event.is_private


async def save_user_data(user_id, key, value):
    await users_collection.update_one(
        {"user_id": user_id},
        {"$set": {key: value}},
        upsert=True
    )
   # print(users_collection)


async def get_user_data_key(user_id, key, default=None):
    user_data = await users_collection.find_one({"user_id": int(user_id)})
  #  print(f"Fetching key '{key}' for user {user_id}: {user_data}")
    return user_data.get(key, default) if user_data else default


async def get_user_data(user_id):
    try:
        user_data = await users_collection.find_one({"user_id": user_id})
        return user_data
    except Exception as e:
   #     logger.error(f"Error retrieving user data for {user_id}: {e}")
        return None


async def save_user_session(user_id, session_string):
    try:
        await users_collection.update_one(
            {"user_id": user_id},
            {"$set": {
                "session_string": session_string,
                "updated_at": datetime.now()
            }},
            upsert=True
        )
        logger.info(f"Saved session for user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving session for user {user_id}: {e}")
        return False


async def remove_user_session(user_id):
    try:
        await users_collection.update_one(
            {"user_id": user_id},
            {"$unset": {"session_string": ""}}
        )
        logger.info(f"Removed session for user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error removing session for user {user_id}: {e}")
        return False


async def save_user_bot(user_id, bot_token):
    try:
        await users_collection.update_one(
            {"user_id": user_id},
            {"$set": {
                "bot_token": bot_token,
                "updated_at": datetime.now()
            }},
            upsert=True
        )
        logger.info(f"Saved bot token for user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error saving bot token for user {user_id}: {e}")
        return False


async def remove_user_bot(user_id):
    try:
        await users_collection.update_one(
            {"user_id": user_id},
            {"$unset": {"bot_token": ""}}
        )
        logger.info(f"Removed bot token for user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error removing bot token for user {user_id}: {e}")
        return False


async def process_text_with_rules(user_id, text):
    if not text:
        return ""
    
    try:
        replacements = await get_user_data_key(user_id, "replacement_words", {})
        delete_words = await get_user_data_key(user_id, "delete_words", [])
        
        processed_text = text
        for word, replacement in replacements.items():
            processed_text = processed_text.replace(word, replacement)
        
        if delete_words:
            words = processed_text.split()
            filtered_words = [w for w in words if w not in delete_words]
            processed_text = " ".join(filtered_words)
        
        return processed_text
    except Exception as e:
        logger.error(f"Error processing text with rules: {e}")
        return text


async def screenshot(video: str, duration: int, sender: str) -> str | None:
    existing_screenshot = f"{sender}.jpg"
    if os.path.exists(existing_screenshot):
        return existing_screenshot

    time_stamp = hhmmss(duration // 2)
    output_file = datetime.now().isoformat("_", "seconds") + ".jpg"

    cmd = [
        "ffmpeg",
        "-ss", time_stamp,
        "-i", video,
        "-frames:v", "1",
        "-vf", "scale='min(320,iw)':'min(320,ih)':force_original_aspect_ratio=decrease",
        output_file,
        "-y"
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    stdout, stderr = await process.communicate()

    if os.path.isfile(output_file):
        return output_file
    else:
        print(f"FFmpeg Error: {stderr.decode().strip()}")
        return None


async def get_video_metadata(file_path):
    default_values = {'width': 1, 'height': 1, 'duration': 1}
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    
    try:
        def _extract_metadata():
            try:
                if not os.path.exists(file_path):
                    logger.error(f"Video file not found: {file_path}")
                    return default_values
                
                if os.path.getsize(file_path) == 0:
                    logger.error(f"Video file is empty: {file_path}")
                    return default_values
                
                os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'
                os.environ['OPENCV_LOG_LEVEL'] = 'ERROR'
                
                cap = cv2.VideoCapture(file_path, cv2.CAP_FFMPEG)
                if not cap.isOpened():
                    logger.warning(f"Could not open with FFMPEG backend, trying ANY: {file_path}")
                    cap = cv2.VideoCapture(file_path, cv2.CAP_ANY)
                
                if not cap.isOpened():
                    logger.warning(f"Could not open video file with any backend: {file_path}")
                    return default_values

                width = round(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

                if fps <= 0 or width <= 0 or height <= 0:
                    cap.release()
                    logger.warning(f"Invalid video properties for: {file_path}")
                    return default_values

                duration = round(frame_count / fps) if frame_count > 0 else 1
                if duration <= 0:
                    duration = 1

                cap.release()
                return {'width': max(1, width), 'height': max(1, height), 'duration': max(1, duration)}
            except Exception as e:
                logger.error(f"Error in video_metadata: {e}")
                return default_values
        
        return await loop.run_in_executor(executor, _extract_metadata)
        
    except Exception as e:
        logger.error(f"Error in get_video_metadata: {e}")
        return default_values


async def validate_and_repair_video(file_path):
    """Validate video file and attempt repair if corrupted"""
    try:
        if not os.path.exists(file_path):
            return False, "File does not exist", file_path

        if os.path.getsize(file_path) < 1024:
            return False, "File too small - likely corrupted", file_path
        
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            logger.warning(f"Cannot open video file, attempting repair: {file_path}")
            cap.release()
            
            repaired_path = f"{file_path}_repaired{os.path.splitext(file_path)[1]}"
            success, result = await repair_video_moov(file_path, repaired_path)
            
            if success:
                if os.path.exists(file_path):
                    os.remove(file_path)
                os.rename(repaired_path, file_path)
                return True, "Video repaired successfully", file_path
            else:
                return False, f"Cannot repair video: {result}", file_path

        ret, frame = cap.read()
        cap.release()

        if not ret:
            logger.warning(f"Cannot read frames, attempting repair: {file_path}")
            
            repaired_path = f"{file_path}_repaired{os.path.splitext(file_path)[1]}"
            success, result = await repair_video_moov(file_path, repaired_path)
            
            if success:
                if os.path.exists(file_path):
                    os.remove(file_path)
                os.rename(repaired_path, file_path)
                return True, "Video repaired successfully", file_path
            else:
                return False, f"Cannot repair video: {result}", file_path

        return True, "Valid video file", file_path

    except Exception as e:
        return False, f"Validation error: {str(e)}", file_path


async def repair_video_moov(input_path, output_path):
    """Fix videos with moov atom issues"""
    try:
        cmd = [
            'ffmpeg', '-i', input_path,
            '-c', 'copy',
            '-movflags', '+faststart',
            '-avoid_negative_ts', 'make_zero',
            '-y', output_path
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0 and os.path.exists(output_path):
            return True, output_path
        else:
            return False, stderr.decode() if stderr else "Unknown error"

    except Exception as e:
        return False, str(e)


async def compress_video(input_path, max_width=1280, max_height=720):
    """Resize video to Telegram standard dimensions (720p - 1280x720) with optimized speed and quality balance"""
    try:
        output_path = f"{os.path.splitext(input_path)[0]}_resized{os.path.splitext(input_path)[1]}"
        
        cmd = [
            'ffmpeg', '-i', input_path,
            '-vf', f'scale=min({max_width}\\,iw):min({max_height}\\,ih):force_original_aspect_ratio=decrease',
            '-c:v', 'libx264',
            '-crf', '20',
            '-preset', 'medium',
            '-c:a', 'copy',
            '-movflags', '+faststart',
            '-y', output_path
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0 and os.path.exists(output_path):
            if os.path.exists(input_path):
                os.remove(input_path)
            os.rename(output_path, input_path)
            return True, "Video resized successfully", input_path
        else:
            return False, stderr.decode() if stderr else "Resize failed", input_path

    except Exception as e:
        return False, str(e), input_path


async def add_premium_user(user_id, duration_value, duration_unit):
    try:
        now = datetime.now()
        expiry_date = None
        
        if duration_unit == "min":
            expiry_date = now + timedelta(minutes=duration_value)
        elif duration_unit == "hours":
            expiry_date = now + timedelta(hours=duration_value)
        elif duration_unit == "days":
            expiry_date = now + timedelta(days=duration_value)
        elif duration_unit == "weeks":
            expiry_date = now + timedelta(weeks=duration_value)
        elif duration_unit == "month":
            expiry_date = now + timedelta(days=30 * duration_value)
        elif duration_unit == "year":
            expiry_date = now + timedelta(days=365 * duration_value)
        elif duration_unit == "decades":
            expiry_date = now + timedelta(days=3650 * duration_value)
        else:
            return False, "Invalid duration unit"
            
        await premium_users_collection.update_one(
            {"user_id": user_id},
            {"$set": {
                "user_id": user_id,
                "subscription_start": now,
                "subscription_end": expiry_date,
                "expireAt": expiry_date
            }},
            upsert=True
        )
        
        await premium_users_collection.create_index("expireAt", expireAfterSeconds=0)
        
        return True, expiry_date
    except Exception as e:
        logger.error(f"Error adding premium user {user_id}: {e}")
        return False, str(e)


async def is_premium_user(user_id):
    try:
        user = await premium_users_collection.find_one({"user_id": user_id})
        if user and "subscription_end" in user:
            now = datetime.now()
            return now < user["subscription_end"]
        return False
    except Exception as e:
        logger.error(f"Error checking premium status for {user_id}: {e}")
        return False


async def get_premium_details(user_id):
    try:
        user = await premium_users_collection.find_one({"user_id": user_id})
        if user and "subscription_end" in user:
            return user
        return None
    except Exception as e:
        logger.error(f"Error getting premium details for {user_id}: {e}")
        return None
