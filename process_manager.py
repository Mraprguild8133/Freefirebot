#!/usr/bin/env python3
"""
Process manager for Free Fire bot with priority scheduling
Manages multiple services with resource allocation
"""

import os
import sys
import signal
import subprocess
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Priority(Enum):
    """Process priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class ServiceConfig:
    """Configuration for a managed service."""
    name: str
    command: str
    priority: Priority
    restart_on_failure: bool = True
    max_restarts: int = 10
    health_check_url: Optional[str] = None
    working_directory: Optional[str] = None

class ProcessManager:
    """Manages multiple processes with priority scheduling."""
    
    def __init__(self):
        self.services: Dict[str, ServiceConfig] = {}
        self.processes: Dict[str, subprocess.Popen] = {}
        self.restart_counts: Dict[str, int] = {}
        self.running = False
        self.executor = ThreadPoolExecutor(max_workers=5)
        
    def add_service(self, service: ServiceConfig):
        """Add a service to be managed."""
        self.services[service.name] = service
        self.restart_counts[service.name] = 0
        logger.info(f"Added service: {service.name} with priority {service.priority.name}")
        
    def start_service(self, service_name: str) -> bool:
        """Start a specific service."""
        if service_name not in self.services:
            logger.error(f"Service {service_name} not found")
            return False
            
        service = self.services[service_name]
        
        try:
            # Set working directory if specified
            cwd = service.working_directory or os.getcwd()
            
            # Start the process
            process = subprocess.Popen(
                service.command,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            self.processes[service_name] = process
            logger.info(f"Started service: {service_name} (PID: {process.pid})")
            
            # Set process priority based on service priority
            self._set_process_priority(process.pid, service.priority)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start service {service_name}: {e}")
            return False
    
    def _set_process_priority(self, pid: int, priority: Priority):
        """Set process priority using OS-specific methods."""
        try:
            import psutil
            process = psutil.Process(pid)
            
            # Map priority levels to OS values
            priority_map = {
                Priority.LOW: psutil.BELOW_NORMAL_PRIORITY_CLASS if os.name == 'nt' else 10,
                Priority.NORMAL: psutil.NORMAL_PRIORITY_CLASS if os.name == 'nt' else 0,
                Priority.HIGH: psutil.ABOVE_NORMAL_PRIORITY_CLASS if os.name == 'nt' else -5,
                Priority.CRITICAL: psutil.HIGH_PRIORITY_CLASS if os.name == 'nt' else -10
            }
            
            if os.name == 'nt':  # Windows
                process.nice(priority_map[priority])
            else:  # Unix-like systems
                os.setpriority(os.PRIO_PROCESS, pid, priority_map[priority])
                
            logger.info(f"Set priority for PID {pid} to {priority.name}")
            
        except ImportError:
            logger.warning("psutil not available, skipping priority setting")
        except Exception as e:
            logger.warning(f"Failed to set priority for PID {pid}: {e}")
    
    def stop_service(self, service_name: str):
        """Stop a specific service."""
        if service_name in self.processes:
            process = self.processes[service_name]
            try:
                process.terminate()
                process.wait(timeout=10)
                logger.info(f"Stopped service: {service_name}")
            except subprocess.TimeoutExpired:
                process.kill()
                logger.warning(f"Force killed service: {service_name}")
            finally:
                del self.processes[service_name]
    
    def restart_service(self, service_name: str):
        """Restart a specific service."""
        logger.info(f"Restarting service: {service_name}")
        self.stop_service(service_name)
        time.sleep(2)  # Brief pause before restart
        self.start_service(service_name)
    
    def monitor_services(self):
        """Monitor all services and restart failed ones."""
        while self.running:
            try:
                for service_name, process in list(self.processes.items()):
                    if process.poll() is not None:  # Process has terminated
                        logger.warning(f"Service {service_name} has stopped")
                        
                        service = self.services[service_name]
                        if service.restart_on_failure:
                            restart_count = self.restart_counts[service_name]
                            if restart_count < service.max_restarts:
                                self.restart_counts[service_name] += 1
                                logger.info(f"Restarting {service_name} (attempt {restart_count + 1})")
                                self.restart_service(service_name)
                            else:
                                logger.error(f"Max restarts exceeded for {service_name}")
                                del self.processes[service_name]
                        else:
                            del self.processes[service_name]
                
                time.sleep(5)  # Check every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in service monitoring: {e}")
                time.sleep(10)
    
    def start_all(self):
        """Start all configured services."""
        self.running = True
        
        # Start services in priority order
        sorted_services = sorted(
            self.services.items(),
            key=lambda x: x[1].priority.value,
            reverse=True
        )
        
        for service_name, service in sorted_services:
            self.start_service(service_name)
            time.sleep(1)  # Brief delay between starts
        
        # Start monitoring in a separate thread
        self.executor.submit(self.monitor_services)
        logger.info("All services started, monitoring active")
    
    def stop_all(self):
        """Stop all services."""
        self.running = False
        
        for service_name in list(self.processes.keys()):
            self.stop_service(service_name)
        
        self.executor.shutdown(wait=True)
        logger.info("All services stopped")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down...")
        self.stop_all()
        sys.exit(0)

def main():
    """Main process manager entry point."""
    manager = ProcessManager()
    
    # Register signal handlers
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)
    
    # Configure services
    services = [
        ServiceConfig(
            name="telegram_bot",
            command="python main.py",
            priority=Priority.CRITICAL,
            restart_on_failure=True,
            max_restarts=10
        ),
        ServiceConfig(
            name="web_interface",
            command="python app.py",
            priority=Priority.HIGH,
            restart_on_failure=True,
            max_restarts=5,
            working_directory="web"
        ),
        ServiceConfig(
            name="health_monitor",
            command="python health_check.py",
            priority=Priority.NORMAL,
            restart_on_failure=True,
            max_restarts=3
        )
    ]
    
    # Add all services
    for service in services:
        manager.add_service(service)
    
    # Start all services
    try:
        manager.start_all()
        
        # Keep main thread alive
        while manager.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt")
    finally:
        manager.stop_all()

if __name__ == "__main__":
    main()