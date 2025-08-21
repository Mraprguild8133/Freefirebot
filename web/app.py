#!/usr/bin/env python3
"""
Web interface for Free Fire Telegram Bot
Displays bot features, commands, and real-time status
"""

from flask import Flask, jsonify, send_from_directory
import os
import sys
from datetime import datetime

app = Flask(__name__, static_folder='.')

# Serve the HTML file
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/api/status')
def bot_status():
    """API endpoint for bot status and live data."""
    return jsonify({
        'status': 'online',
        'last_update': datetime.now().isoformat(),
        'features': {
            'live_updates': True,
            'gun_sensitivity': True,
            'character_abilities': True,
            'recoil_control': True,
            'real_time_sync': True
        },
        'commands': [
            '/firebutton - Complete gun sensitivity guide',
            '/sensitivity - Detailed sensitivity settings', 
            '/recoil - Recoil control patterns',
            '/characters - Character information',
            '/abilities - Character combinations',
            '/updates - Latest game updates',
            '/events - Current events',
            '/help - Complete command guide'
        ],
        'stats': {
            'weapons_covered': 30,
            'characters': 25,
            'commands_available': 8,
            'update_frequency': '30 seconds'
        }
    })

if __name__ == '__main__':
    # Run on port 5000 for Replit environment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)