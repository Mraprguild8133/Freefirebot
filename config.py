"""
Configuration settings for the Free Fire Telegram Bot
"""

import os

# Bot configuration
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
if not BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

# API Keys for external services (if needed)
FREE_FIRE_API_KEY = os.getenv("FREE_FIRE_API_KEY", "")
GARENA_API_KEY = os.getenv("GARENA_API_KEY", "")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Bot settings
BOT_NAME = "Free Fire Updates Bot"
BOT_VERSION = "1.0.0"

# API endpoints (placeholder for real endpoints)
FREE_FIRE_API_BASE = "https://api.freefire.example.com"
GARENA_API_BASE = "https://api.garena.com"

# Cache settings
CACHE_TIMEOUT = 60  # 1 minute for real-time updates
LIVE_UPDATE_INTERVAL = 30  # Check website every 30 seconds

# Message limits
MAX_MESSAGE_LENGTH = 4096
