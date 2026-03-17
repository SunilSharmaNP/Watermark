"""
Configuration file for Telegram Bot
Store all credentials and settings here
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Credentials
API_ID = int(os.getenv("API_ID", ""))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Admin user ID for restricted commands
ADMIN_ID = int(os.getenv("ADMIN_ID", "0")) if os.getenv("ADMIN_ID") else None

# Updater Configuration
UPSTREAM_REPO = os.getenv("UPSTREAM_REPO", "").strip()
UPSTREAM_BRANCH = os.getenv("UPSTREAM_BRANCH", "main").strip()
UPDATE_PKGS = os.getenv("UPDATE_PKGS", "True").lower() == "true"

# Storage settings
STORAGE_PATH = "user_data"
LOGOS_PATH = os.path.join(STORAGE_PATH, "logos")
SETTINGS_PATH = os.path.join(STORAGE_PATH, "settings")
TEMP_PATH = os.path.join(STORAGE_PATH, "temp")

# Image settings
THUMBNAIL_MAX_SIZE = 4000
LOGO_MAX_SIZE = 5000
QUALITY = 95

# Create directories if they don't exist
for directory in [STORAGE_PATH, LOGOS_PATH, SETTINGS_PATH, TEMP_PATH]:
    os.makedirs(directory, exist_ok=True)
