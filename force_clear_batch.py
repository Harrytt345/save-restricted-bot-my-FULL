#!/usr/bin/env python3
# Force clear all batch operations

import json
import os

# Clear the active users file
with open('active_users.json', 'w') as f:
    json.dump({}, f)

print("✅ Cleared active_users.json")

# Clear any temp download files
downloads = os.listdir('downloads')
for file in downloads:
    try:
        file_path = os.path.join('downloads', file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"✅ Deleted: {file}")
    except Exception as e:
        print(f"❌ Error deleting {file}: {e}")

print("\n✅ All batch operations cleared!")
print("⚠️  Please restart the bot to reload the cleared state.")
