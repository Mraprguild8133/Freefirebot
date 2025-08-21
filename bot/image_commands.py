"""
Image command handlers for Free Fire Telegram Bot
Dedicated handlers for image-related commands
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.image_handler import fire_image_handler
from bot.utils import format_error_message

logger = logging.getLogger(__name__)

async def weapon_image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /weapon_image command to show weapon images."""
    try:
        user_id = update.effective_user.id
        logger.info(f"User {user_id} requested weapon images")
        
        if not context.args:
            # Show available weapons
            available_weapons = fire_image_handler.get_available_weapon_images()
            weapon_list = "\n".join([f"• {weapon.upper()}" for weapon in available_weapons])
            
            message = (
                "🎯 <b>Weapon Images Available</b>\n\n"
                f"{weapon_list}\n\n"
                "<b>Usage:</b> /weapon_image [weapon_name]\n"
                "<b>Example:</b> /weapon_image ak47\n\n"
                "Or use /weapon_gallery to see all weapons at once!"
            )
            await update.message.reply_text(message, parse_mode='HTML')
            return
        
        weapon_name = " ".join(context.args).lower()
        success = await fire_image_handler.send_weapon_image(update, context, weapon_name)
        
        if not success:
            await update.message.reply_text(
                f"❌ No image found for weapon: {weapon_name}\n"
                "Use /weapon_image without arguments to see available weapons."
            )
            
    except Exception as e:
        logger.error(f"Error in weapon_image_handler: {e}")
        error_msg = format_error_message("showing weapon image")
        await update.message.reply_text(error_msg)

async def character_image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /character_image command to show character images."""
    try:
        user_id = update.effective_user.id
        logger.info(f"User {user_id} requested character images")
        
        if not context.args:
            # Show available characters
            available_characters = fire_image_handler.get_available_character_images()
            character_list = "\n".join([f"• {char.title().replace('_', ' ')}" for char in available_characters])
            
            message = (
                "👤 <b>Character Images Available</b>\n\n"
                f"{character_list}\n\n"
                "<b>Usage:</b> /character_image [character_name]\n"
                "<b>Example:</b> /character_image alok\n\n"
                "Or use /character_gallery to see all characters at once!"
            )
            await update.message.reply_text(message, parse_mode='HTML')
            return
        
        character_name = " ".join(context.args).lower()
        success = await fire_image_handler.send_character_image(update, context, character_name)
        
        if not success:
            await update.message.reply_text(
                f"❌ No image found for character: {character_name}\n"
                "Use /character_image without arguments to see available characters."
            )
            
    except Exception as e:
        logger.error(f"Error in character_image_handler: {e}")
        error_msg = format_error_message("showing character image")
        await update.message.reply_text(error_msg)

async def weapon_gallery_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /weapon_gallery command to show weapon gallery."""
    try:
        user_id = update.effective_user.id
        logger.info(f"User {user_id} requested weapon gallery")
        
        # Send loading message
        loading_msg = await update.message.reply_text("🎯 Loading weapon gallery...")
        
        # Get all available weapons
        weapons = fire_image_handler.get_available_weapon_images()
        success = await fire_image_handler.send_weapon_gallery(update, context, weapons)
        
        # Delete loading message
        await loading_msg.delete()
        
        if success:
            await update.message.reply_text(
                "🎯 <b>Free Fire Weapons Gallery</b>\n\n"
                "All available weapon images with specifications.\n"
                "Use /weapon_image [name] for individual weapons.",
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text(
                "❌ Unable to load weapon gallery at the moment. Please try again later."
            )
            
    except Exception as e:
        logger.error(f"Error in weapon_gallery_handler: {e}")
        error_msg = format_error_message("showing weapon gallery")
        await update.message.reply_text(error_msg)

async def character_gallery_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /character_gallery command to show character gallery."""
    try:
        user_id = update.effective_user.id
        logger.info(f"User {user_id} requested character gallery")
        
        # Send loading message
        loading_msg = await update.message.reply_text("👤 Loading character gallery...")
        
        # Get all available characters
        characters = fire_image_handler.get_available_character_images()
        success = await fire_image_handler.send_character_gallery(update, context, characters)
        
        # Delete loading message
        await loading_msg.delete()
        
        if success:
            await update.message.reply_text(
                "👤 <b>Free Fire Characters Gallery</b>\n\n"
                "All available character images with abilities.\n"
                "Use /character_image [name] for individual characters.",
                parse_mode='HTML'
            )
        else:
            await update.message.reply_text(
                "❌ Unable to load character gallery at the moment. Please try again later."
            )
            
    except Exception as e:
        logger.error(f"Error in character_gallery_handler: {e}")
        error_msg = format_error_message("showing character gallery")
        await update.message.reply_text(error_msg)

async def guide_image_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /guide_image command to show gameplay guide images."""
    try:
        user_id = update.effective_user.id
        logger.info(f"User {user_id} requested guide images")
        
        if not context.args:
            # Show available guides
            available_guides = fire_image_handler.get_available_guide_images()
            guide_list = "\n".join([f"• {guide.title().replace('_', ' ')}" for guide in available_guides])
            
            message = (
                "📱 <b>Gameplay Guide Images Available</b>\n\n"
                f"{guide_list}\n\n"
                "<b>Usage:</b> /guide_image [guide_name]\n"
                "<b>Example:</b> /guide_image sensitivity_guide\n\n"
                "These visual guides help optimize your gameplay settings!"
            )
            await update.message.reply_text(message, parse_mode='HTML')
            return
        
        guide_name = "_".join(context.args).lower()
        success = await fire_image_handler.send_gameplay_guide_image(update, context, guide_name)
        
        if not success:
            await update.message.reply_text(
                f"❌ No guide image found for: {guide_name}\n"
                "Use /guide_image without arguments to see available guides."
            )
            
    except Exception as e:
        logger.error(f"Error in guide_image_handler: {e}")
        error_msg = format_error_message("showing guide image")
        await update.message.reply_text(error_msg)