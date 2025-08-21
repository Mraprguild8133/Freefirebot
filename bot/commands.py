"""
Command logic and message generation for the Free Fire bot
"""

import logging
from datetime import datetime
from bot.data_service import FreefireDataService
from bot.utils import format_timestamp

logger = logging.getLogger(__name__)
data_service = FreefireDataService()


def get_start_message(user_name: str) -> str:
    """Generate welcome message for /start command."""
    return (
        f"🔥 <b>Welcome to Free Fire Updates Bot, {user_name}!</b>\n\n"
        "🎮 Get the latest Free Fire updates, events, and character information!\n\n"
        "<b>Available Commands:</b>\n"
        "• /updates - Latest game updates and version info\n"
        "• /events - Current and upcoming events\n"
        "• /characters - Character information and abilities\n"
        "• /firebutton - Fire button controls and tips\n"
        "• /weapon_gallery - View all weapon images\n"
        "• /character_gallery - View all character images\n"
        "• /help - Show this help message\n\n"
        "🚀 Start exploring by using any of the commands above!"
    )


def get_help_message() -> str:
    """Generate help message with all available commands."""
    return (
        "🔥 <b>Free Fire Updates Bot - Help</b>\n\n"
        "<b>📱 Available Commands:</b>\n\n"
        "<b>📋 Main Commands:</b>\n"
        "<b>/start</b> - Welcome message and quick start\n"
        "<b>/updates</b> - Latest Free Fire updates and version info\n"
        "<b>/events</b> - Current and upcoming events calendar\n"
        "<b>/characters</b> - Character information and abilities\n"
        "<b>/firebutton</b> - Fire button controls and optimization tips\n"
        "<b>/help</b> - Show this help message\n\n"
        "<b>🖼️ Image Commands:</b>\n"
        "<b>/weapon_gallery</b> - View all weapon images\n"
        "<b>/character_gallery</b> - View all character images\n"
        "<b>/weapon_image [name]</b> - Show specific weapon image\n"
        "<b>/character_image [name]</b> - Show specific character image\n"
        "<b>/guide_image [type]</b> - Show gameplay guide images\n\n"
        "<b>🔄 Aliases:</b>\n"
        "<b>/sensitivity</b> - Same as /firebutton\n"
        "<b>/recoil</b> - Same as /firebutton\n"
        "<b>/abilities</b> - Same as /characters\n"
        "<b>/version</b> - Same as /updates\n\n"
        "🎯 <b>Tips:</b>\n"
        "• Commands are case-sensitive\n"
        "• Information is updated regularly\n"
        "• Report issues to bot administrators\n\n"
        "🔥 <i>Stay updated with the latest Free Fire content!</i>"
    )


async def get_updates_info() -> str:
    """Fetch and format Free Fire updates information."""
    try:
        updates = await data_service.get_latest_updates()
        
        if not updates:
            return (
                "📱 <b>Free Fire Updates</b>\n\n"
                "❌ <b>No Update Information Available</b>\n\n"
                "Unable to retrieve update information at this time. This could be due to:\n"
                "• Temporary service unavailability\n"
                "• Network connectivity issues\n"
                "• API service maintenance\n\n"
                "Please try again in a few minutes."
            )
        
        message = "📱 <b>Free Fire - Latest Updates</b>\n\n"
        
        for update in updates:
            message += (
                f"🔥 <b>{update.get('title', 'Update')}</b>\n"
                f"📅 <b>Version:</b> {update.get('version', 'Unknown')}\n"
                f"📅 <b>Release Date:</b> {update.get('release_date', 'TBD')}\n"
                f"📝 <b>Description:</b>\n{update.get('description', 'No description available')}\n\n"
            )
            
            if update.get('features'):
                message += "<b>✨ New Features:</b>\n"
                for feature in update['features']:
                    message += f"• {feature}\n"
                message += "\n"
        
        message += f"🕒 <i>Last updated: {format_timestamp(datetime.now())}</i>"
        return message
        
    except Exception as e:
        logger.error(f"Error fetching updates: {e}")
        return (
            "📱 <b>Free Fire Updates</b>\n\n"
            "❌ <b>Service Error</b>\n\n"
            "Unable to fetch update information due to a service error. "
            "The development team has been notified.\n\n"
            "Please try again later."
        )


async def get_events_info() -> str:
    """Fetch and format Free Fire events information."""
    try:
        events = await data_service.get_current_events()
        
        if not events:
            return (
                "📅 <b>Free Fire Events Calendar</b>\n\n"
                "❌ <b>No Event Information Available</b>\n\n"
                "Unable to retrieve event information at this time. This could be due to:\n"
                "• Temporary service unavailability\n"
                "• No active events currently\n"
                "• API service maintenance\n\n"
                "Please check back later for upcoming events."
            )
        
        message = "📅 <b>Free Fire - Events Calendar</b>\n\n"
        
        for event in events:
            status = "🔴 LIVE" if event.get('is_active') else "🟡 UPCOMING"
            message += (
                f"{status} <b>{event.get('name', 'Unnamed Event')}</b>\n"
                f"📅 <b>Start:</b> {event.get('start_date', 'TBD')}\n"
                f"📅 <b>End:</b> {event.get('end_date', 'TBD')}\n"
                f"🎁 <b>Rewards:</b> {event.get('rewards', 'Various rewards')}\n"
                f"📝 <b>Description:</b>\n{event.get('description', 'No description available')}\n\n"
            )
        
        message += f"🕒 <i>Last updated: {format_timestamp(datetime.now())}</i>"
        return message
        
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        return (
            "📅 <b>Free Fire Events Calendar</b>\n\n"
            "❌ <b>Service Error</b>\n\n"
            "Unable to fetch event information due to a service error. "
            "The development team has been notified.\n\n"
            "Please try again later."
        )


async def get_characters_info() -> str:
    """Fetch and format Free Fire characters information."""
    try:
        characters = await data_service.get_characters_info()
        
        if not characters:
            return (
                "👤 <b>Free Fire Characters</b>\n\n"
                "❌ <b>No Character Information Available</b>\n\n"
                "Unable to retrieve character information at this time. This could be due to:\n"
                "• Temporary service unavailability\n"
                "• API service maintenance\n"
                "• Network connectivity issues\n\n"
                "Please try again in a few minutes."
            )
        
        message = "👤 <b>Free Fire - Character Information</b>\n\n"
        
        for character in characters:
            message += (
                f"🔥 <b>{character.get('name', 'Unknown Character')}</b>\n"
                f"⭐ <b>Ability:</b> {character.get('ability_name', 'Unknown')}\n"
                f"📝 <b>Description:</b> {character.get('ability_description', 'No description available')}\n"
                f"🎯 <b>Type:</b> {character.get('ability_type', 'Unknown')}\n"
            )
            
            if character.get('is_new'):
                message += "🆕 <b>NEW CHARACTER!</b>\n"
            
            message += "\n"
        
        message += f"🕒 <i>Last updated: {format_timestamp(datetime.now())}</i>"
        return message
        
    except Exception as e:
        logger.error(f"Error fetching characters: {e}")
        return (
            "👤 <b>Free Fire Characters</b>\n\n"
            "❌ <b>Service Error</b>\n\n"
            "Unable to fetch character information due to a service error. "
            "The development team has been notified.\n\n"
            "Please try again later."
        )


def get_gun_sensitivity_info() -> str:
    """Generate comprehensive gun sensitivity and recoil settings."""
    return (
        "🎯 <b>Complete Gun Sensitivity Guide</b>\n\n"
        "<b>🔫 ASSAULT RIFLES:</b>\n"
        "• <b>AK47:</b> Gen:75, Red:70, 2x:65, 4x:55\n"
        "• <b>AN94:</b> Gen:80, Red:75, 2x:70, 4x:60\n"
        "• <b>SCAR:</b> Gen:85, Red:80, 2x:75, 4x:65\n"
        "• <b>M4A1:</b> Gen:82, Red:78, 2x:72, 4x:62\n"
        "• <b>AUG:</b> Gen:78, Red:73, 2x:68, 4x:58\n\n"
        "<b>🔫 SMG:</b>\n"
        "• <b>MP40:</b> Gen:90, Red:85, 2x:80\n"
        "• <b>Thompson:</b> Gen:88, Red:83, 2x:78\n"
        "• <b>Vector:</b> Gen:85, Red:80, 2x:75\n"
        "• <b>P90:</b> Gen:87, Red:82, 2x:77\n\n"
        "<b>🎯 SNIPERS:</b>\n"
        "• <b>AWM:</b> Gen:70, 2x:60, 4x:50, 8x:40\n"
        "• <b>Kar98k:</b> Gen:72, 2x:62, 4x:52, 8x:42\n"
        "• <b>M82B:</b> Gen:68, 2x:58, 4x:48, 8x:38\n\n"
        "Use /sensitivity for detailed recoil patterns!"
    )

def get_character_abilities_info() -> str:
    """Generate character ability combinations and details."""
    return (
        "👤 <b>Character Ability Combinations</b>\n\n"
        "<b>🔥 TOP COMBINATIONS:</b>\n\n"
        "<b>🎯 ASSAULT COMBO:</b>\n"
        "• <b>Chrono:</b> Time shield + speed boost\n"
        "• <b>Jota:</b> Sustained fire damage boost\n"
        "• <b>Hayato:</b> Armor penetration increase\n"
        "• <b>Luqueta:</b> Hat trick damage bonus\n\n"
        "<b>🏃 RUSH COMBO:</b>\n"
        "• <b>Kelly:</b> Increased sprint speed\n"
        "• <b>Joseph:</b> Movement speed boost\n"
        "• <b>Moco:</b> Enemy marking ability\n"
        "• <b>Shirou:</b> Damage tracking\n\n"
        "<b>🛡️ SUPPORT COMBO:</b>\n"
        "• <b>Alok:</b> Healing + speed aura\n"
        "• <b>DJ Alok:</b> Drop the beat healing\n"
        "• <b>Dimitri:</b> Healing zone creation\n"
        "• <b>Thiva:</b> Armor rescue boost\n\n"
        "Use /abilities for complete ability details!"
    )

def get_recoil_patterns_info() -> str:
    """Generate detailed recoil control patterns."""
    return (
        "⚡ <b>Recoil Control Patterns</b>\n\n"
        "<b>🔫 WEAPON RECOIL PATTERNS:</b>\n\n"
        "<b>AK47:</b> Heavy recoil - Pull down + left\n"
        "<b>M4A1:</b> Moderate - Straight down control\n"
        "<b>SCAR:</b> Light - Down + slight right\n"
        "<b>Vector:</b> High fire rate - Rapid down pulls\n"
        "<b>AN94:</b> Burst control - Short down pulls\n\n"
        "<b>📱 DEVICE ADJUSTMENTS:</b>\n"
        "• <b>Phone (5-6\"):</b> +5 to all sensitivity\n"
        "• <b>Tablet (7\"+):</b> -5 to all sensitivity\n"
        "• <b>High refresh:</b> +3 to all values\n\n"
        "<b>🎮 FIRE BUTTON SETTINGS:</b>\n"
        "• <b>Size:</b> 130-150 for better control\n"
        "• <b>Auto Fire:</b> ON for SMG/AR, OFF for Sniper\n"
        "• <b>Peek & Fire:</b> Enable for advanced play\n\n"
        "Practice in training ground first!"
    )
