#!/bin/bash
# Docker deployment script for Free Fire Bot with mean priority

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.yml"
PROJECT_NAME="firebot"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_requirements() {
    log_info "Checking Docker requirements..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    log_success "Docker requirements satisfied"
}

check_environment() {
    log_info "Checking environment variables..."
    
    if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
        log_error "TELEGRAM_BOT_TOKEN environment variable is required"
        echo "Please set it with: export TELEGRAM_BOT_TOKEN='your_bot_token'"
        exit 1
    fi
    
    if [ -z "$FREE_FIRE_API_KEY" ]; then
        log_warning "FREE_FIRE_API_KEY not set (optional)"
    fi
    
    if [ -z "$GARENA_API_KEY" ]; then
        log_warning "GARENA_API_KEY not set (optional)"
    fi
    
    log_success "Environment variables checked"
}

build_images() {
    log_info "Building Docker images with mean priority settings..."
    
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME build --no-cache
    
    if [ $? -eq 0 ]; then
        log_success "Docker images built successfully"
    else
        log_error "Failed to build Docker images"
        exit 1
    fi
}

start_services() {
    log_info "Starting Free Fire Bot services with priority allocation..."
    
    # Start services in priority order
    log_info "Starting Redis (cache service)..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d redis
    
    log_info "Starting monitoring services..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d monitoring
    
    log_info "Starting main Free Fire Bot (critical priority)..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d firebot
    
    log_info "Starting Nginx reverse proxy..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d nginx
    
    if [ $? -eq 0 ]; then
        log_success "All services started successfully"
    else
        log_error "Failed to start services"
        exit 1
    fi
}

show_status() {
    log_info "Service status:"
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME ps
    
    echo ""
    log_info "Service endpoints:"
    echo "  Web Interface: http://localhost:5000"
    echo "  Health Check:  http://localhost:8080/health"
    echo "  Monitoring:    http://localhost:9090"
    echo "  Main Site:     http://localhost"
}

stop_services() {
    log_info "Stopping Free Fire Bot services..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down
    log_success "Services stopped"
}

restart_services() {
    log_info "Restarting Free Fire Bot services..."
    stop_services
    start_services
    show_status
}

show_logs() {
    local service=${1:-firebot}
    log_info "Showing logs for service: $service"
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f $service
}

cleanup() {
    log_info "Cleaning up Docker resources..."
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down -v --rmi all
    docker system prune -f
    log_success "Cleanup completed"
}

# Main script
case "$1" in
    start)
        check_requirements
        check_environment
        build_images
        start_services
        show_status
        ;;
    stop)
        stop_services
        ;;
    restart)
        check_requirements
        restart_services
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs $2
        ;;
    build)
        check_requirements
        build_images
        ;;
    cleanup)
        cleanup
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs [service]|build|cleanup}"
        echo ""
        echo "Commands:"
        echo "  start    - Build and start all services with mean priority"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  status   - Show service status and endpoints"
        echo "  logs     - Show logs (optionally for specific service)"
        echo "  build    - Build Docker images only"
        echo "  cleanup  - Stop services and remove all Docker resources"
        echo ""
        echo "Examples:"
        echo "  $0 start              # Start all services"
        echo "  $0 logs firebot       # Show Free Fire Bot logs"
        echo "  $0 logs               # Show all logs"
        exit 1
        ;;
esac