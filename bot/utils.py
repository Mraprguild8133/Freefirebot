"""
Utility functions for the Free Fire Telegram bot
"""

import re
from datetime import datetime
from typing import List
from config import MAX_MESSAGE_LENGTH


def split_long_message(message: str, max_length: int = MAX_MESSAGE_LENGTH) -> List[str]:
    """
    Split a long message into smaller chunks that fit Telegram's message limit.
    
    Args:
        message: The message to split
        max_length: Maximum length per message chunk
    
    Returns:
        List of message chunks
    """
    if len(message) <= max_length:
        return [message]
    
    chunks = []
    current_chunk = ""
    
    # Split by lines to maintain formatting
    lines = message.split('\n')
    
    for line in lines:
        # Check if adding this line would exceed the limit
        if len(current_chunk) + len(line) + 1 > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
        
        # If a single line is too long, split it by words
        if len(line) > max_length:
            words = line.split(' ')
            temp_line = ""
            
            for word in words:
                if len(temp_line) + len(word) + 1 > max_length:
                    if temp_line:
                        current_chunk += temp_line + '\n'
                        temp_line = ""
                    
                    # If a single word is too long, truncate it
                    if len(word) > max_length:
                        word = word[:max_length-3] + "..."
                
                temp_line += word + " "
            
            current_chunk += temp_line.strip() + '\n'
        else:
            current_chunk += line + '\n'
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


def format_timestamp(dt: datetime) -> str:
    """
    Format a datetime object into a readable string.
    
    Args:
        dt: Datetime object to format
    
    Returns:
        Formatted datetime string
    """
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")


def format_error_message(action: str) -> str:
    """
    Generate a formatted error message for failed actions.
    
    Args:
        action: The action that failed (e.g., "fetching updates")
    
    Returns:
        Formatted error message
    """
    return (
        f"❌ <b>Error</b>\n\n"
        f"Failed to complete the requested action: {action}\n\n"
        "<b>Possible causes:</b>\n"
        "• Temporary service unavailability\n"
        "• Network connectivity issues\n"
        "• External API maintenance\n\n"
        "Please try again in a few minutes. If the problem persists, "
        "please contact the bot administrators."
    )


def sanitize_html(text: str) -> str:
    """
    Sanitize text for safe HTML display in Telegram messages.
    
    Args:
        text: Text to sanitize
    
    Returns:
        Sanitized text
    """
    # Replace potentially dangerous HTML characters
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('&', '&amp;')
    
    return text


def extract_command_args(message_text: str) -> List[str]:
    """
    Extract arguments from a command message.
    
    Args:
        message_text: Full message text including command
    
    Returns:
        List of command arguments
    """
    # Remove the command part and split by spaces
    parts = message_text.split()[1:]  # Skip the command itself
    return [arg.strip() for arg in parts if arg.strip()]


def validate_date_format(date_string: str) -> bool:
    """
    Validate if a date string is in the expected format.
    
    Args:
        date_string: Date string to validate
    
    Returns:
        True if valid, False otherwise
    """
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def format_duration(start_date: str, end_date: str) -> str:
    """
    Calculate and format duration between two dates.
    
    Args:
        start_date: Start date string
        end_date: End date string
    
    Returns:
        Formatted duration string
    """
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        duration = end - start
        
        if duration.days == 0:
            return "Less than 1 day"
        elif duration.days == 1:
            return "1 day"
        else:
            return f"{duration.days} days"
    except ValueError:
        return "Duration unavailable"


def escape_markdown(text: str) -> str:
    """
    Escape special characters for Markdown formatting.
    
    Args:
        text: Text to escape
    
    Returns:
        Escaped text safe for Markdown
    """
    # Characters that need escaping in Telegram MarkdownV2
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    
    return text


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length with optional suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: Suffix to add if text is truncated
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix
