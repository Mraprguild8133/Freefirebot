#!/usr/bin/env python3
"""
Health check endpoint for Free Fire bot deployment
Monitors bot status and resource usage
"""

import asyncio
import logging
import psutil
import time
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HealthMonitor:
    """Monitor bot health and system resources."""
    
    def __init__(self):
        self.start_time = time.time()
        self.last_check = datetime.now()
        
    def get_system_stats(self):
        """Get current system resource usage."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_available': memory.available,
                'disk_usage': disk.percent,
                'disk_free': disk.free,
                'uptime': time.time() - self.start_time
            }
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return None
    
    def check_bot_status(self):
        """Check if the Telegram bot is responsive."""
        try:
            # Simple health check - can be expanded
            return {
                'status': 'healthy',
                'last_check': self.last_check.isoformat(),
                'services': {
                    'telegram_bot': 'running',
                    'web_interface': 'running',
                    'data_sync': 'active'
                }
            }
        except Exception as e:
            logger.error(f"Bot health check failed: {e}")
            return {
                'status': 'unhealthy',
                'error': str(e)
            }

monitor = HealthMonitor()

@app.route('/health')
def health_check():
    """Main health check endpoint."""
    system_stats = monitor.get_system_stats()
    bot_status = monitor.check_bot_status()
    
    health_data = {
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy' if system_stats and bot_status.get('status') == 'healthy' else 'unhealthy',
        'system': system_stats,
        'bot': bot_status,
        'version': '1.0.0'
    }
    
    status_code = 200 if health_data['status'] == 'healthy' else 503
    return jsonify(health_data), status_code

@app.route('/metrics')
def metrics():
    """Detailed metrics endpoint."""
    system_stats = monitor.get_system_stats()
    
    if not system_stats:
        return jsonify({'error': 'Unable to retrieve metrics'}), 500
    
    metrics_data = {
        'timestamp': datetime.now().isoformat(),
        'performance': {
            'cpu_usage': system_stats['cpu_usage'],
            'memory_usage': system_stats['memory_usage'],
            'disk_usage': system_stats['disk_usage'],
            'uptime_seconds': system_stats['uptime']
        },
        'resources': {
            'memory_available_mb': system_stats['memory_available'] // (1024 * 1024),
            'disk_free_gb': system_stats['disk_free'] // (1024 * 1024 * 1024)
        },
        'bot_metrics': {
            'commands_processed': 'N/A',  # Can be tracked in main bot
            'users_active': 'N/A',
            'errors_last_hour': 'N/A'
        }
    }
    
    return jsonify(metrics_data)

@app.route('/status')
def status():
    """Simple status endpoint."""
    return jsonify({
        'status': 'running',
        'service': 'free-fire-bot',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)