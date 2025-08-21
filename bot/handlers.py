"""
Handler functions for Telegram bot commands
"""

import logging
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from bot.commands import (
    get_start_message,
    get_help_message,
    get_updates_info,
    get_events_info,
    get_characters_info,
    get_gun_sensitivity_info,
    get_character_abilities_info,
    get_recoil_patterns_info
)
from bot.utils import split_long_message, format_error_message

logger = logging.getLogger(__name__)


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command."""
    try:
        user = update.effective_user
        logger.info(f"User {user.id} ({user.username}) started the bot")
        
        message = get_start_message(user.first_name)
        await update.message.reply_text(message, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error in start_handler: {e}")
        await update.message.reply_text(
            "❌ Sorry, there was an error processing your request. Please try again later."
        )


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command."""
    try:
        message = get_help_message()
        await update.message.reply_text(message, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error in help_handler: {e}")
        await update.message.reply_text(
            "❌ Sorry, there was an error showing help information. Please try again later."
        )


async def updates_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /updates command."""
    try:
        logger.info(f"User {update.effective_user.id} requested updates")
        
        # Show loading message
        loading_msg = await update.message.reply_text("🔍 Fetching latest Free Fire updates...")
        
        updates_info = await get_updates_info()
        
        # Delete loading message
        await loading_msg.delete()
        
        if updates_info:
            # Split long messages if necessary
            messages = split_long_message(updates_info)
            for msg in messages:
                await update.message.reply_text(msg, parse_mode='HTML')
        else:
            await update.message.reply_text(
                "❌ Unable to fetch update information at the moment. Please try again later."
            )
            
    except Exception as e:
        logger.error(f"Error in updates_handler: {e}")
        error_msg = format_error_message("fetching updates")
        await update.message.reply_text(error_msg)


async def events_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /events command."""
    try:
        logger.info(f"User {update.effective_user.id} requested events")
        
        # Show loading message
        loading_msg = await update.message.reply_text("📅 Loading event calendar...")
        
        events_info = await get_events_info()
        
        # Delete loading message
        await loading_msg.delete()
        
        if events_info:
            messages = split_long_message(events_info)
            for msg in messages:
                await update.message.reply_text(msg, parse_mode='HTML')
        else:
            await update.message.reply_text(
                "❌ Unable to fetch event information at the moment. Please try again later."
            )
            
    except Exception as e:
        logger.error(f"Error in events_handler: {e}")
        error_msg = format_error_message("fetching events")
        await update.message.reply_text(error_msg)


async def characters_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /characters command."""
    try:
        logger.info(f"User {update.effective_user.id} requested character info")
        
        # Show loading message
        loading_msg = await update.message.reply_text("👤 Loading character information...")
        
        characters_info = await get_characters_info()
        
        # Delete loading message
        await loading_msg.delete()
        
        if characters_info:
            messages = split_long_message(characters_info)
            for msg in messages:
                await update.message.reply_text(msg, parse_mode='HTML')
        else:
            await update.message.reply_text(
                "❌ Unable to fetch character information at the moment. Please try again later."
            )
            
    except Exception as e:
        logger.error(f"Error in characters_handler: {e}")
        error_msg = format_error_message("fetching character information")
        await update.message.reply_text(error_msg)


async def fire_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /firebutton command."""
    try:
        logger.info(f"User {update.effective_user.id} requested fire button info")
        
        # Send comprehensive gun sensitivity info
        gun_message = get_gun_sensitivity_info()
        await update.message.reply_text(gun_message, parse_mode='HTML')
        
        # Send character abilities info after short delay
        await asyncio.sleep(1)
        character_message = get_character_abilities_info()
        await update.message.reply_text(character_message, parse_mode='HTML')
        
        # Send recoil patterns info after short delay
        await asyncio.sleep(1)
        recoil_message = get_recoil_patterns_info()
        await update.message.reply_text(recoil_message, parse_mode='HTML')
        
    except Exception as e:
        logger.error(f"Error in fire_button_handler: {e}")
        error_msg = format_error_message("fetching fire button information")
        await update.message.reply_text(error_msg)


async def unknown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle unknown commands."""
    command = update.message.text
    logger.info(f"User {update.effective_user.id} sent unknown command: {command}")
    
    message = (
        "❓ <b>Unknown Command</b>\n\n"
        f"Sorry, I don't recognize the command: <code>{command}</code>\n\n"
        "Use /help to see all available commands."
    )
    await update.message.reply_text(message, parse_mode='HTML')


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors that occur during bot operation."""
    logger.error(f"Exception while handling an update: {context.error}")
    
    if isinstance(update, Update) and update.message:
        error_msg = (
            "❌ <b>Unexpected Error</b>\n\n"
            "An unexpected error occurred while processing your request. "
            "Please try again in a few moments.\n\n"
            "If the problem persists, the bot administrators have been notified."
        )
        try:
            await update.message.reply_text(error_msg, parse_mode='HTML')
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
