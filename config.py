# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import os
from dotenv import load_dotenv
from pathlib import Path

# Only load .env if it exists, and don't override Replit secrets
if Path('.env').exists():
    load_dotenv(override=False)

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID_STR = os.getenv("API_ID")
API_ID = int(API_ID_STR) if API_ID_STR else 0
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_DB = os.getenv("MONGO_DB", "")
OWNER_ID = [int(x) for x in os.getenv("OWNER_ID", "").split() if x] if os.getenv("OWNER_ID") else []
DB_NAME = os.getenv("DB_NAME", "telegram_downloader")
STRING = os.getenv("STRING", None) # optional
LOG_GROUP_STR = os.getenv("LOG_GROUP")
LOG_GROUP = int(LOG_GROUP_STR) if LOG_GROUP_STR else None # optional with -100
FORCE_SUB_STR = os.getenv("FORCE_SUB")
FORCE_SUB = int(FORCE_SUB_STR) if FORCE_SUB_STR else None # optional with -100
MASTER_KEY = os.getenv("MASTER_KEY", "gK8HzLfT9QpViJcYeB5wRa3DmN7P2xUq") # for session encryption
IV_KEY = os.getenv("IV_KEY", "s7Yx5CpVmE3F") # for decryption
YT_COOKIES = os.getenv("YT_COOKIES", YTUB_COOKIES)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", INST_COOKIES)
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT = int(os.getenv("PREMIUM_LIMIT", "500"))
JOIN_LINK = os.getenv("JOIN_LINK", "tg://user?id=7385595817") # this link for start command message
ADMIN_CONTACT = os.getenv("ADMIN_CONTACT", "tg://user?id=7385595817")


# PREMIUM PLANS CONFIGURATION
P0 = {
    "d": {
        "s": int(os.getenv("PLAN_D_S", "1")),
        "du": int(os.getenv("PLAN_D_DU", "1")),
        "u": os.getenv("PLAN_D_U", "days"),
        "l": os.getenv("PLAN_D_L", "Daily"),
    },
    "w": {
        "s": int(os.getenv("PLAN_W_S", "3")),
        "du": int(os.getenv("PLAN_W_DU", "1")),
        "u": os.getenv("PLAN_W_U", "weeks"),
        "l": os.getenv("PLAN_W_L", "Weekly"),
    },
    "m": {
        "s": int(os.getenv("PLAN_M_S", "5")),
        "du": int(os.getenv("PLAN_M_DU", "1")),
        "u": os.getenv("PLAN_M_U", "month"),
        "l": os.getenv("PLAN_M_L", "Monthly"),
    },
}
