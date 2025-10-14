# Save Restricted Content Bot V3

## Project Overview
A Telegram bot that retrieves restricted messages from Telegram channels and groups. It features custom thumbnail support, 4GB file uploads, and downloads from YouTube, Instagram, Facebook, and 100+ other sites.

## Tech Stack
- **Language**: Python 3.11
- **Bot Framework**: Pyrogram v2 (custom build) + Telethon
- **Web Framework**: Flask (welcome page on port 5000)
- **Database**: MongoDB
- **External Libraries**: yt-dlp, devgagantools, opencv, aiofiles

## Project Structure
```
/
├── plugins/          # Bot command handlers
├── templates/        # Flask HTML templates
├── utils/           # Helper functions and filters
├── main.py          # Main bot entry point
├── app.py           # Flask web server
├── shared_client.py # Telegram client initialization
├── config.py        # Configuration from env variables
├── kk.py           # String session generator
└── start.sh        # Startup script (Flask + Bot)
```

## Key Features
- Extract content from public/private channels/groups
- Custom bot functionality
- 128-bit encryption for data
- Session-based login
- Custom captions and thumbnails
- 4GB file upload support (with premium string)
- File splitter for non-premium
- Premium user priority queue
- Topic support for group uploads
- Real-time download/upload progress

## Setup & Configuration

### Required Environment Variables
- `API_ID` - Telegram API ID
- `API_HASH` - Telegram API Hash
- `BOT_TOKEN` - Bot token from @BotFather
- `MONGO_DB` - MongoDB connection URL
- `OWNER_ID` - Owner Telegram user ID (space-separated list)
- `LOG_GROUP` - Group ID for logging (optional)
- `FORCE_SUB` - Channel ID for forced subscription (optional)

### Optional Variables
- `STRING` - Premium account session string (for 4GB uploads)
- `FREEMIUM_LIMIT` - Free user extraction limit (default: 0)
- `PREMIUM_LIMIT` - Premium batch limit (default: 500)
- `YT_COOKIES` - YouTube cookies for downloading
- `INSTA_COOKIES` - Instagram cookies for downloading

## Workflows
- **Bot**: Runs both Flask app (port 5000) and Telegram bot via `start.sh`

## Recent Changes (Oct 14, 2025)
- Installed Python 3.11 and all dependencies
- Created `kk.py` - Pyrogram v2 string session generator
- Added `.gitignore` for Python project
- Created `start.sh` to run both Flask and bot together
- Configured workflow to bind Flask to port 5000
- Set up all environment variables via Replit Secrets
- Configured OWNER_ID as 7385595817 with premium access
- Removed all Team SPY branding and replaced with neutral text
- Updated all contact links to direct to owner user ID
- Created `autosetup.py` to auto-configure BotFather-style command menu on startup
- Updated config defaults (JOIN_LINK, ADMIN_CONTACT) to owner contact

### Critical Video Processing Fixes (Oct 14, 2025)
- **Fixed download path issue** - Removed problematic downloads directory structure
- **Added P0 premium configuration** - Added missing premium plans config
- **Enhanced video metadata extraction** - Improved OpenCV backend selection (FFMPEG → ANY fallback)
- **Added video validation & repair** - Automatically detects and repairs corrupted videos
- **Integrated FFmpeg repair** - Fixes moov atom errors and JPEG2000 codec issues
- **Config fixes** - Fixed LOG_GROUP and FORCE_SUB to handle empty values properly
- All OpenCV errors (icvExtractPattern, moov atom not found) now handled gracefully

### New /reset Command Feature (Oct 14, 2025)
- **Added /reset command** - Owner-only command to immediately clear all active batch operations
  - Unlike /stop (which waits for current batch to complete), /reset instantly clears all operations
  - Clears ACTIVE_USERS dictionary and active_users.json file
  - Resets all user states (Z dictionary) to prepare for next batch
  - Validates and reports missing config.py credentials (API_ID, API_HASH, BOT_TOKEN, MONGO_DB)
  - Added to bot command menu and README documentation
  - Provides feedback on number of cleared operations and credential status

### Video Resizing Feature (Oct 14, 2025)
- **Automatic video resizing to Telegram standard dimensions (720p - 1280x720)**
  - All videos are now automatically resized to match Telegram's standard format
  - Reduces video dimensions with visually lossless quality (CRF 18)
  - Uses FFmpeg with H.264 codec and slow preset for maximum quality
  - Audio codec copied without re-encoding to preserve original quality
  - Maintains aspect ratio while resizing dimensions
  - Note: Dimension resizing requires video re-encoding, but uses highest quality settings
  - Applied to both regular uploads and large files (>2GB)
  - Shows "Resizing video..." status during processing

## Deployment

### Render Deployment
The bot can be deployed on Render using Docker:
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Render will automatically detect the Dockerfile
4. Configure environment variables in Render dashboard:
   - `API_ID`, `API_HASH`, `BOT_TOKEN`, `MONGO_DB`, `OWNER_ID`
   - Optional: `STRING`, `LOG_GROUP`, `FORCE_SUB`, `YT_COOKIES`, `INSTA_COOKIES`
5. The bot will automatically bind to Render's PORT environment variable
6. Optionally use the included `render.yaml` for Infrastructure as Code deployment

**Features for Render:**
- Automatic session file cleanup on startup (prevents conflicts with multiple instances)
- PORT environment variable detection (works with Render's dynamic port assignment)
- Health check endpoint at root URL (`/`)
- Optimized Docker image with multi-stage caching

### Docker Deployment
```bash
docker build -t telegram-bot .
docker run -p 5000:5000 --env-file .env telegram-bot
```
The Dockerfile is optimized for Render and automatically detects the PORT environment variable.

## Development Notes
- Flask serves a welcome page showing "TEAM SPY - Bot is Live"
- Bot automatically starts Telethon (SpyLib) and Pyrogram clients
- Optional userbot client starts only if STRING session is provided
- Session files are gitignored for security

## Usage
- Run `python kk.py` to generate a new Pyrogram v2 session string
- The bot automatically handles login flows for users
- Commands available: /start, /batch, /login, /logout, /dl, /adl, /session, /settings, etc.

## Author
Developed by devgagan and TEAM SPY
