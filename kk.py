#!/usr/bin/env python3
# String Session Generator for Pyrogram v2
# Copyright (c) 2025 devgagan : https://github.com/devgaganin.

from pyrogram import Client
import asyncio

async def main():
    print("\n=== Pyrogram v2 String Session Generator ===\n")
    
    api_id = input("Enter your API_ID: ")
    api_hash = input("Enter your API_HASH: ")
    
    if not api_id or not api_hash:
        print("\nError: API_ID and API_HASH are required!")
        return
    
    try:
        api_id = int(api_id)
    except ValueError:
        print("\nError: API_ID must be a number!")
        return
    
    print("\nGenerating session string...")
    print("You will receive an OTP on your Telegram account.\n")
    
    async with Client(
        name="string_session",
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True
    ) as app:
        session_string = await app.export_session_string()
        
        print("\n" + "="*60)
        print("Your Pyrogram v2 Session String:")
        print("="*60)
        print(f"\n{session_string}\n")
        print("="*60)
        print("\nSave this session string securely!")
        print("You can use it in the STRING environment variable.\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n\nError: {e}")
