# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from shared_client import app
from pyrogram.types import BotCommand

async def run_autosetup_plugin():
    try:
        await app.set_bot_commands([
            BotCommand("start", "🚀 Start the bot"),
            BotCommand("batch", "🫠 Extract in bulk"),
            BotCommand("login", "🔑 Get into the bot"),
            BotCommand("setbot", "🧸 Add your bot for handling files"),
            BotCommand("logout", "🚪 Get out of the bot"),
            BotCommand("adl", "👻 Download audio from 30+ sites"),
            BotCommand("dl", "💀 Download videos from 30+ sites"),
            BotCommand("status", "⟳ Refresh Payment status"),
            BotCommand("transfer", "💘 Gift premium to others"),
            BotCommand("add", "➕ Add user to premium"),
            BotCommand("rem", "➖ Remove from premium"),
            BotCommand("rembot", "🤨 Remove your custom bot"),
            BotCommand("settings", "⚙️ Personalize things"),
            BotCommand("plan", "🗓️ Check our premium plans"),
            BotCommand("terms", "🥺 Terms and conditions"),
            BotCommand("help", "❓ If you're a noob, still!"),
            BotCommand("cancel", "🚫 Cancel login/batch/settings process"),
            BotCommand("stop", "🚫 Cancel batch process")
        ])
        print("✅ Bot commands menu configured successfully! (BotFather style)")
    except Exception as e:
        print(f"⚠️ Error setting up bot commands: {e}")
