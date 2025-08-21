"""
Image handling for Free Fire Telegram Bot
Manages character images, weapon images, and gameplay screenshots
"""

import os
import logging
from typing import Optional, Dict, List
from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class FireImageHandler:
    """Handles Free Fire images and media content."""
    
    def __init__(self):
        self.character_images = {
            # Main Characters with official artwork URLs
            "alok": "https://ff.garena.com/files/characters/alok.jpg",
            "chrono": "https://ff.garena.com/files/characters/chrono.jpg", 
            "kelly": "https://ff.garena.com/files/characters/kelly.jpg",
            "hayato": "https://ff.garena.com/files/characters/hayato.jpg",
            "jota": "https://ff.garena.com/files/characters/jota.jpg",
            "dimitri": "https://ff.garena.com/files/characters/dimitri.jpg",
            "dj_alok": "https://ff.garena.com/files/characters/dj_alok.jpg",
            "joseph": "https://ff.garena.com/files/characters/joseph.jpg",
            "moco": "https://ff.garena.com/files/characters/moco.jpg",
            "shirou": "https://ff.garena.com/files/characters/shirou.jpg",
            "thiva": "https://ff.garena.com/files/characters/thiva.jpg",
            "luqueta": "https://ff.garena.com/files/characters/luqueta.jpg"
        }
        
        self.weapon_images = {
            # Assault Rifles
            "ak47": "https://ff.garena.com/files/weapons/ak47.jpg",
            "m4a1": "https://ff.garena.com/files/weapons/m4a1.jpg",
            "scar": "https://ff.garena.com/files/weapons/scar.jpg",
            "an94": "https://ff.garena.com/files/weapons/an94.jpg",
            "aug": "https://ff.garena.com/files/weapons/aug.jpg",
            
            # Sniper Rifles
            "awm": "https://ff.garena.com/files/weapons/awm.jpg",
            "kar98k": "https://ff.garena.com/files/weapons/kar98k.jpg",
            "m82b": "https://ff.garena.com/files/weapons/m82b.jpg",
            
            # SMGs
            "mp40": "https://ff.garena.com/files/weapons/mp40.jpg",
            "thompson": "https://ff.garena.com/files/weapons/thompson.jpg",
            "vector": "https://ff.garena.com/files/weapons/vector.jpg",
            "p90": "https://ff.garena.com/files/weapons/p90.jpg"
        }
        
        self.gameplay_images = {
            "sensitivity_guide": "https://ff.garena.com/files/guides/sensitivity.jpg",
            "recoil_patterns": "https://ff.garena.com/files/guides/recoil.jpg",
            "fire_button_setup": "https://ff.garena.com/files/guides/firebutton.jpg",
            "character_combinations": "https://ff.garena.com/files/guides/combinations.jpg"
        }

    async def send_character_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE, character_name: str) -> bool:
        """Send character image with information."""
        try:
            character_key = character_name.lower().replace(" ", "_")
            image_url = self.character_images.get(character_key)
            
            if image_url:
                caption = f"🔥 <b>{character_name.title()}</b>\n\nOfficial Free Fire character artwork"
                await update.message.reply_photo(
                    photo=image_url,
                    caption=caption,
                    parse_mode='HTML'
                )
                return True
            else:
                logger.warning(f"No image found for character: {character_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending character image for {character_name}: {e}")
            return False

    async def send_weapon_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE, weapon_name: str) -> bool:
        """Send weapon image with specifications."""
        try:
            weapon_key = weapon_name.lower().replace(" ", "_")
            image_url = self.weapon_images.get(weapon_key)
            
            if image_url:
                caption = f"🎯 <b>{weapon_name.upper()}</b>\n\nOfficial weapon artwork with specifications"
                await update.message.reply_photo(
                    photo=image_url,
                    caption=caption,
                    parse_mode='HTML'
                )
                return True
            else:
                logger.warning(f"No image found for weapon: {weapon_name}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending weapon image for {weapon_name}: {e}")
            return False

    async def send_gameplay_guide_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE, guide_type: str) -> bool:
        """Send gameplay guide images."""
        try:
            guide_key = guide_type.lower().replace(" ", "_")
            image_url = self.gameplay_images.get(guide_key)
            
            if image_url:
                caption = f"📱 <b>{guide_type.title()}</b>\n\nVisual guide for optimal gameplay settings"
                await update.message.reply_photo(
                    photo=image_url,
                    caption=caption,
                    parse_mode='HTML'
                )
                return True
            else:
                logger.warning(f"No image found for guide: {guide_type}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending guide image for {guide_type}: {e}")
            return False

    async def send_character_gallery(self, update: Update, context: ContextTypes.DEFAULT_TYPE, characters: List[str]) -> bool:
        """Send a gallery of character images."""
        try:
            media_group = []
            for i, character in enumerate(characters[:10]):  # Limit to 10 images per gallery
                character_key = character.lower().replace(" ", "_")
                image_url = self.character_images.get(character_key)
                
                if image_url:
                    caption = f"{character.title()}" if i == 0 else None
                    media_group.append(
                        InputMediaPhoto(
                            media=image_url,
                            caption=caption
                        )
                    )
            
            if media_group:
                await update.message.reply_media_group(media=media_group)
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error sending character gallery: {e}")
            return False

    async def send_weapon_gallery(self, update: Update, context: ContextTypes.DEFAULT_TYPE, weapons: List[str]) -> bool:
        """Send a gallery of weapon images."""
        try:
            media_group = []
            for i, weapon in enumerate(weapons[:10]):  # Limit to 10 images per gallery
                weapon_key = weapon.lower().replace(" ", "_")
                image_url = self.weapon_images.get(weapon_key)
                
                if image_url:
                    caption = f"🎯 {weapon.upper()}" if i == 0 else None
                    media_group.append(
                        InputMediaPhoto(
                            media=image_url,
                            caption=caption
                        )
                    )
            
            if media_group:
                await update.message.reply_media_group(media=media_group)
                return True
            else:
                return False
                
        except Exception as e:
            logger.error(f"Error sending weapon gallery: {e}")
            return False

    def get_available_character_images(self) -> List[str]:
        """Get list of available character images."""
        return list(self.character_images.keys())

    def get_available_weapon_images(self) -> List[str]:
        """Get list of available weapon images."""
        return list(self.weapon_images.keys())

    def get_available_guide_images(self) -> List[str]:
        """Get list of available guide images."""
        return list(self.gameplay_images.keys())

# Global instance
fire_image_handler = FireImageHandler()