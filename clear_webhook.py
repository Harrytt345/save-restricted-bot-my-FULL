#!/usr/bin/env python3
# Script to clear webhooks for the bot

import urllib.request
import urllib.parse
import json
from config import BOT_TOKEN

def clear_webhooks():
    print("Clearing webhooks...")
    
    # Use Telegram Bot API directly to delete webhook
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook?drop_pending_updates=True"
        
        response = urllib.request.urlopen(url)
        result = json.loads(response.read().decode())
        
        if result.get("ok"):
            print("✅ Webhook cleared successfully!")
            print("   Bot is now using long polling mode.")
        else:
            print(f"❌ Failed to clear webhook: {result.get('description', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Error clearing webhook: {e}")
    
    print("\n✅ Webhook cleanup complete!")

if __name__ == "__main__":
    clear_webhooks()
