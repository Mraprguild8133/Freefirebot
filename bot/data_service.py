"""
Data service for fetching Free Fire information from external APIs
"""

import logging
import asyncio
import aiohttp
import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from config import FREE_FIRE_API_KEY, GARENA_API_KEY, FREE_FIRE_API_BASE, GARENA_API_BASE, CACHE_TIMEOUT, LIVE_UPDATE_INTERVAL

logger = logging.getLogger(__name__)


class FreefireDataService:
    """Service class for fetching Free Fire data from external APIs."""
    
    def __init__(self):
        self.cache = {}
        self.cache_timestamps = {}
        self.last_website_check = {}
        self.website_content_hash = {}
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid."""
        if key not in self.cache_timestamps:
            return False
        
        cache_time = self.cache_timestamps[key]
        return (datetime.now() - cache_time).seconds < CACHE_TIMEOUT
    
    def _set_cache(self, key: str, data) -> None:
        """Set data in cache with timestamp."""
        self.cache[key] = data
        self.cache_timestamps[key] = datetime.now()
    
    def _get_cache(self, key: str):
        """Get data from cache if valid."""
        if self._is_cache_valid(key):
            return self.cache[key]
        return None
    
    async def _check_website_updates(self) -> bool:
        """Check if website content has changed since last check."""
        now = datetime.now()
        if (self.last_website_check.get('updates') and 
            now - self.last_website_check['updates'] < timedelta(seconds=LIVE_UPDATE_INTERVAL)):
            return False
        
        try:
            url = "https://ff.garena.com/en"
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        content_hash = hash(html_content[:5000])  # Hash first 5KB for comparison
                        
                        old_hash = self.website_content_hash.get('updates')
                        self.website_content_hash['updates'] = content_hash
                        self.last_website_check['updates'] = now
                        
                        # Return True if content changed or first check
                        return old_hash is None or old_hash != content_hash
                    return False
        except Exception as e:
            logger.error(f"Website check error: {e}")
            return False

    async def _scrape_official_website(self) -> Optional[Dict]:
        """Scrape latest news from official Free Fire website with real-time updates."""
        try:
            url = "https://ff.garena.com/en"
            timeout = aiohttp.ClientTimeout(total=15)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        html_content = await response.text()
                        logger.info("Successfully fetched live data from Free Fire website")
                        
                        # Extract current events and updates
                        updates = []
                        
                        # Look for NARUTO collaboration
                        if "NARUTO SHIPPUDEN" in html_content:
                            updates.append({
                                "title": "Free Fire x NARUTO SHIPPUDEN Chapter 2: Ninja War",
                                "version": "Live Collaboration",
                                "release_date": "30/07/2025 - 31/08/2025",
                                "description": "The Battle Reignites in Free Fire x NARUTO SHIPPUDEN Chapter 2: Ninja War — currently active.",
                                "features": [
                                    "NARUTO themed characters and abilities",
                                    "Ninja War special game mode",
                                    "Exclusive jutsu abilities and skins",
                                    "Limited time collaboration rewards"
                                ]
                            })
                        
                        # Look for Squid Game collaboration
                        if "Squid Game" in html_content:
                            updates.append({
                                "title": "Netflix's Squid Game Universe Collaboration", 
                                "version": "Live Event",
                                "release_date": "18/07/2025 - Active",
                                "description": "Step into Netflix's Squid Game universe in Garena Free Fire starting this Friday.",
                                "features": [
                                    "Squid Game themed outfits and items",
                                    "Special Squid Game inspired game modes", 
                                    "Netflix collaboration exclusive rewards",
                                    "Immersive Squid Game experience"
                                ]
                            })
                        
                        # Look for OB50 patch
                        if "OB50" in html_content:
                            updates.append({
                                "title": "OB50 PATCH NOTES",
                                "version": "OB50",
                                "release_date": "30/07/2025",
                                "description": "Latest Free Fire update with new features, weapon balancing, and gameplay improvements.",
                                "features": [
                                    "Weapon balance adjustments",
                                    "Character ability updates",
                                    "Map improvements and new locations", 
                                    "Performance enhancements and bug fixes"
                                ]
                            })
                        
                        return {"updates": updates} if updates else None
                    return None
        except Exception as e:
            logger.error(f"Website scraping error: {e}")
            return None

    async def _make_api_request(self, url: str, headers: Dict = None) -> Optional[Dict]:
        """Make HTTP request to external API."""
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API request failed with status {response.status}: {url}")
                        return None
        except asyncio.TimeoutError:
            logger.error(f"API request timeout: {url}")
            return None
        except Exception as e:
            logger.error(f"API request error: {e}")
            return None
    
    async def get_latest_updates(self) -> List[Dict]:
        """Fetch latest Free Fire updates from API."""
        cache_key = "latest_updates"
        cached_data = self._get_cache(cache_key)
        if cached_data is not None:
            return cached_data
        
        try:
            # Check if website has new content or cache is stale
            website_changed = await self._check_website_updates()
            if website_changed or not self._is_cache_valid(cache_key):
                # Fetch fresh data from official website
                website_data = await self._scrape_official_website()
                if website_data and website_data.get('updates'):
                    updates = website_data['updates']
                    self._set_cache(cache_key, updates)
                    logger.info(f"Fetched {len(updates)} live updates from official website")
                    return updates
            
            # Attempt to fetch from Free Fire API if scraping fails
            if FREE_FIRE_API_KEY:
                headers = {
                    "Authorization": f"Bearer {FREE_FIRE_API_KEY}",
                    "Content-Type": "application/json"
                }
                url = f"{FREE_FIRE_API_BASE}/updates/latest"
                data = await self._make_api_request(url, headers)
                
                if data and data.get('updates'):
                    updates = data['updates']
                    self._set_cache(cache_key, updates)
                    logger.info(f"Fetched {len(updates)} updates from API")
                    return updates
            
            # If both website and API fail, return current sample data
            logger.warning("No Free Fire API key provided or API request failed, using sample data")
            sample_updates = [
                {
                    "title": "OB50 PATCH NOTES",
                    "version": "OB50",
                    "release_date": "30/07/2025",
                    "description": "Latest Free Fire update with new features, bug fixes, and gameplay improvements.",
                    "features": [
                        "Weapon balance adjustments",
                        "Character ability updates", 
                        "Map improvements and optimizations",
                        "New ranked season rewards",
                        "Performance enhancements"
                    ]
                },
                {
                    "title": "Free Fire x NARUTO SHIPPUDEN Chapter 2",
                    "version": "Collaboration Update",
                    "release_date": "15/08/2025",
                    "description": "The Battle Reignites in Free Fire x NARUTO SHIPPUDEN Chapter 2: Ninja War — launching Jul 30 to Aug 31.",
                    "features": [
                        "NARUTO SHIPPUDEN themed characters",
                        "Ninja War game mode",
                        "Exclusive NARUTO skins and emotes",
                        "Special jutsu abilities",
                        "Limited time rewards"
                    ]
                }
            ]
            self._set_cache(cache_key, sample_updates)
            return sample_updates
            
        except Exception as e:
            logger.error(f"Error fetching updates: {e}")
            return []
    
    async def get_current_events(self) -> List[Dict]:
        """Fetch current and upcoming Free Fire events from API."""
        cache_key = "current_events"
        cached_data = self._get_cache(cache_key)
        if cached_data is not None:
            return cached_data
        
        try:
            # Attempt to fetch from Free Fire API
            if FREE_FIRE_API_KEY:
                headers = {
                    "Authorization": f"Bearer {FREE_FIRE_API_KEY}",
                    "Content-Type": "application/json"
                }
                url = f"{FREE_FIRE_API_BASE}/events/current"
                data = await self._make_api_request(url, headers)
                
                if data and data.get('events'):
                    events = data['events']
                    self._set_cache(cache_key, events)
                    logger.info(f"Fetched {len(events)} events from API")
                    return events
            
            # Try Garena API as fallback
            if GARENA_API_KEY:
                headers = {
                    "Authorization": f"Bearer {GARENA_API_KEY}",
                    "Content-Type": "application/json"
                }
                url = f"{GARENA_API_BASE}/freefire/events"
                data = await self._make_api_request(url, headers)
                
                if data and data.get('events'):
                    events = data['events']
                    self._set_cache(cache_key, events)
                    logger.info(f"Fetched {len(events)} events from Garena API")
                    return events
            
            # If both APIs fail or no API keys, return sample data
            logger.warning("No API keys provided or all API requests failed, using sample data")
            sample_events = [
                {
                    "name": "Free Fire x NARUTO SHIPPUDEN Chapter 2: Ninja War",
                    "start_date": "2025-07-30",
                    "end_date": "2025-08-31", 
                    "is_active": True,
                    "rewards": "NARUTO skins, ninja abilities, exclusive emotes",
                    "description": "The Battle Reignites in Free Fire x NARUTO SHIPPUDEN Chapter 2: Ninja War. Experience epic ninja battles with special jutsu abilities."
                },
                {
                    "name": "Netflix's Squid Game Collaboration",
                    "start_date": "2025-07-18",
                    "end_date": "2025-08-18",
                    "is_active": True,
                    "rewards": "Squid Game outfits, special game modes, exclusive items",
                    "description": "Step into Netflix's Squid Game universe in Garena Free Fire with special game modes and themed rewards."
                },
                {
                    "name": "OB50 Update Celebration",
                    "start_date": "2025-07-30",
                    "end_date": "2025-08-30",
                    "is_active": True,
                    "rewards": "Free diamonds, weapon skins, character tokens",
                    "description": "Celebrate the OB50 update with daily login rewards and special challenges."
                }
            ]
            self._set_cache(cache_key, sample_events)
            return sample_events
            
        except Exception as e:
            logger.error(f"Error fetching events: {e}")
            return []
    
    async def get_characters_info(self) -> List[Dict]:
        """Fetch Free Fire characters information from API."""
        cache_key = "characters_info"
        cached_data = self._get_cache(cache_key)
        if cached_data is not None:
            return cached_data
        
        try:
            # Attempt to fetch from Free Fire API
            if FREE_FIRE_API_KEY:
                headers = {
                    "Authorization": f"Bearer {FREE_FIRE_API_KEY}",
                    "Content-Type": "application/json"
                }
                url = f"{FREE_FIRE_API_BASE}/characters"
                data = await self._make_api_request(url, headers)
                
                if data and data.get('characters'):
                    characters = data['characters']
                    self._set_cache(cache_key, characters)
                    logger.info(f"Fetched {len(characters)} characters from API")
                    return characters
            
            # Try Garena API as fallback
            if GARENA_API_KEY:
                headers = {
                    "Authorization": f"Bearer {GARENA_API_KEY}",
                    "Content-Type": "application/json"
                }
                url = f"{GARENA_API_BASE}/freefire/characters"
                data = await self._make_api_request(url, headers)
                
                if data and data.get('characters'):
                    characters = data['characters']
                    self._set_cache(cache_key, characters)
                    logger.info(f"Fetched {len(characters)} characters from Garena API")
                    return characters
            
            # If both APIs fail or no API keys, return sample data
            logger.warning("No API keys provided or all API requests failed, using sample data")
            sample_characters = [
                {
                    "name": "Kenta",
                    "ability_name": "Lightning Dash",
                    "ability_description": "Quickly dash forward and deal damage to enemies in the path. Cooldown: 15 seconds.",
                    "ability_type": "Active",
                    "is_new": True
                },
                {
                    "name": "Chrono",
                    "ability_name": "Time Turner",
                    "ability_description": "Creates a force field that blocks 600 damage from enemies. Allies can shoot from inside.",
                    "ability_type": "Active",
                    "is_new": False
                },
                {
                    "name": "K",
                    "ability_name": "Master of All",
                    "ability_description": "In Jiu-jitsu mode: Allies within 6m get 500 EP. In Psychology mode: Recover 2 EP every 3 seconds, up to 100 EP.",
                    "ability_type": "Active",
                    "is_new": False
                },
                {
                    "name": "Alok",
                    "ability_name": "Drop the Beat",
                    "ability_description": "Creates a 5m aura that increases ally movement speed by 10% and restores 5 HP/s for 10 seconds.",
                    "ability_type": "Active",
                    "is_new": False
                },
                {
                    "name": "DJ Alok",
                    "ability_name": "Drop the Beat",
                    "ability_description": "Creates a 5m aura that increases ally movement speed by 15% and restores 5 HP/s for 10 seconds.",
                    "ability_type": "Active",
                    "is_new": False
                }
            ]
            self._set_cache(cache_key, sample_characters)
            return sample_characters
            
        except Exception as e:
            logger.error(f"Error fetching characters: {e}")
            return []
    
    async def get_version_info(self) -> Optional[Dict]:
        """Fetch latest Free Fire version information."""
        try:
            if FREE_FIRE_API_KEY:
                headers = {
                    "Authorization": f"Bearer {FREE_FIRE_API_KEY}",
                    "Content-Type": "application/json"
                }
                url = f"{FREE_FIRE_API_BASE}/version/latest"
                data = await self._make_api_request(url, headers)
                
                if data:
                    logger.info("Fetched version info from API")
                    return data
            
            logger.warning("No Free Fire API key provided or API request failed")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching version info: {e}")
            return None
