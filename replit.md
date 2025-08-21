# Free Fire Telegram Bot

## Overview

This is a Telegram bot that provides Free Fire game updates, events, and character information to users. The bot serves as an information hub for Free Fire players, offering real-time updates about game versions, current events, character abilities, and gameplay tips through Telegram commands.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Technology**: Python with `python-telegram-bot` library
- **Architecture Pattern**: Command-based handler system with modular design
- **Deployment**: Dual deployment support - optimized for Replit and Docker with priority resource allocation and process management
- **Rationale**: The bot uses a handler-based architecture where each command is processed by dedicated handler functions, providing clean separation of concerns and easy extensibility

### Command System
- **Structure**: Centralized command routing through `main.py` with dedicated handlers
- **Available Commands**: `/start`, `/help`, `/updates`, `/events`, `/characters`, `/firebutton`, `/version`
- **Image Commands**: `/weapon_gallery`, `/character_gallery`, `/weapon_image [name]`, `/character_image [name]`, `/guide_image [type]`
- **Command Aliases**: `/sensitivity`, `/recoil`, `/abilities` for enhanced user accessibility
- **Error Handling**: Comprehensive error handling with user-friendly error messages and detailed logging

### Data Management
- **Service Layer**: `FreefireDataService` class handles external data sources
- **Primary Data Source**: Official Free Fire website scraping for live updates
- **Fallback Sources**: Free Fire and Garena APIs as secondary options
- **Caching Strategy**: In-memory caching with configurable timeout (1 minute for real-time)
- **Live Data Integration**: Real-time scraping from https://ff.garena.com/en for current events and updates
- **Synchronization**: Bot checks website every 30 seconds and updates immediately when content changes

### Configuration Management
- **Environment Variables**: All sensitive data (API keys, bot tokens) stored as environment variables
- **Centralized Config**: Single `config.py` file manages all application settings
- **Security**: Bot token validation ensures proper configuration before startup

### Message Processing
- **Message Formatting**: HTML parsing for rich text formatting in Telegram messages
- **Long Message Handling**: Automatic message splitting to comply with Telegram's 4096 character limit
- **User Experience**: Personalized welcome messages and context-aware responses
- **Image Support**: Comprehensive image handling for characters, weapons, and gameplay guides
- **Media Galleries**: Support for sending multiple images as media groups

## External Dependencies

### Required Services
- **Telegram Bot API**: Core messaging platform integration requiring `TELEGRAM_BOT_TOKEN`
- **Free Fire API**: Game data source requiring `FREE_FIRE_API_KEY` (placeholder endpoints)
- **Garena API**: Additional game information requiring `GARENA_API_KEY`

### Python Libraries
- **python-telegram-bot**: Telegram Bot API wrapper for handling bot interactions
- **aiohttp**: Async HTTP client for external API requests
- **asyncio**: Async programming support for non-blocking operations

### Infrastructure Requirements
- **Environment Variables**: Must configure bot token and API keys
- **Network Access**: Requires outbound HTTPS connections to Telegram and game APIs
- **Logging**: Structured logging system with configurable log levels
- **Process Management**: Priority-based service management with health monitoring
- **Resource Allocation**: Optimized memory and CPU usage with auto-scaling capabilities
- **Health Monitoring**: Comprehensive health checks and metrics collection
- **Docker Support**: Complete containerized deployment with mean priority scheduling
- **Service Orchestration**: Multi-service architecture with Redis, Nginx, and monitoring
- **Load Balancing**: Nginx reverse proxy with SSL termination and rate limiting