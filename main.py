#!/usr/bin/env python3
"""
Free Fire Telegram Bot - Main Entry Point
Provides Free Fire game updates, events, and character information
"""

import logging
import asyncio
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import BOT_TOKEN, LOG_LEVEL
from bot.handlers import (
    start_handler,
    help_handler,
    updates_handler,
    events_handler,
    characters_handler,
    fire_button_handler,
    unknown_handler,
    error_handler
)
from bot.image_commands import (
    weapon_image_handler,
    character_image_handler,
    weapon_gallery_handler,
    character_gallery_handler,
    guide_image_handler
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL.upper(), logging.INFO)
)
logger = logging.getLogger(__name__)


def main():
    """Initialize and start the Telegram bot."""
    # Create the Application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("updates", updates_handler))
    app.add_handler(CommandHandler("events", events_handler))
    app.add_handler(CommandHandler("characters", characters_handler))
    app.add_handler(CommandHandler("firebutton", fire_button_handler))
    app.add_handler(CommandHandler("sensitivity", fire_button_handler))  # Alias for firebutton
    app.add_handler(CommandHandler("recoil", fire_button_handler))  # Alias for firebutton
    app.add_handler(CommandHandler("abilities", characters_handler))  # Alias for characters
    app.add_handler(CommandHandler("version", updates_handler))  # Alias for updates
    
    # Image commands
    app.add_handler(CommandHandler("weapon_image", weapon_image_handler))
    app.add_handler(CommandHandler("character_image", character_image_handler))
    app.add_handler(CommandHandler("weapon_gallery", weapon_gallery_handler))
    app.add_handler(CommandHandler("character_gallery", character_gallery_handler))
    app.add_handler(CommandHandler("guide_image", guide_image_handler))
    
    # Register message handlers for unknown commands
    app.add_handler(MessageHandler(filters.COMMAND, unknown_handler))
    
    # Register error handler
    app.add_error_handler(error_handler)
    
    logger.info("Starting Free Fire Telegram Bot...")
    
    # Start the bot
    app.run_polling(allowed_updates=["message", "callback_query"])


if __name__ == '__main__':
    main()
