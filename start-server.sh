#!/bin/bash

# 🚀 Binhtoi Inventory Management - Pinterest Style
# Server Startup Script

echo "🎨 Binhtoi Inventory Management - Pinterest Style"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Function to start with Docker
start_docker() {
    echo "🐳 Starting with Docker..."
    
    # Check if container exists
    if docker ps -a --format "table {{.Names}}" | grep -q "binhtoi-webapp-1"; then
        echo "📦 Container exists, restarting..."
        docker-compose restart webapp
    else
        echo "📦 Creating new container..."
        docker-compose up -d webapp
    fi
    
    # Wait for container to be ready
    echo "⏳ Waiting for server to start..."
    sleep 3
    
    # Check if container is running
    if docker ps --format "table {{.Names}}" | grep -q "binhtoi-webapp-1"; then
        echo "✅ Docker container started successfully!"
        echo "🌐 Pinterest-style app: http://localhost:8000"
        echo "📊 Container status:"
        docker ps --filter "name=binhtoi-webapp-1" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    else
        echo "❌ Failed to start Docker container"
        docker logs binhtoi-webapp-1 --tail 10
        exit 1
    fi
}

# Function to start with Python
start_python() {
    echo "🐍 Starting with Python..."
    
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 is not installed"
        exit 1
    fi
    
    # Check if requirements are installed
    if ! python3 -c "import supabase" 2>/dev/null; then
        echo "📦 Installing requirements..."
        pip3 install -r requirements.txt
    fi
    
    # Start Python server
    echo "🚀 Starting Python HTTP server..."
    python3 -m http.server 8001 &
    SERVER_PID=$!
    
    echo "✅ Python server started successfully!"
    echo "🌐 Pinterest-style app: http://localhost:8001"
    echo "🔧 Server PID: $SERVER_PID"
    echo "⏹️  To stop: kill $SERVER_PID"
}

# Main menu
echo ""
echo "Choose startup method:"
echo "1) Docker (Recommended) - Port 8000"
echo "2) Python HTTP Server - Port 8001"
echo "3) Check current status"
echo "4) Stop all servers"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        start_docker
        ;;
    2)
        start_python
        ;;
    3)
        echo "📊 Current Status:"
        echo ""
        echo "🐳 Docker Containers:"
        docker ps --filter "name=binhtoi" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" || echo "No Docker containers running"
        echo ""
        echo "🐍 Python Processes:"
        ps aux | grep -E "(python.*server|http.server)" | grep -v grep || echo "No Python servers running"
        ;;
    4)
        echo "🛑 Stopping all servers..."
        
        # Stop Docker container
        if docker ps --format "table {{.Names}}" | grep -q "binhtoi-webapp-1"; then
            echo "🐳 Stopping Docker container..."
            docker-compose stop webapp
        fi
        
        # Stop Python servers
        pkill -f "python.*http.server" 2>/dev/null && echo "🐍 Stopped Python servers"
        
        echo "✅ All servers stopped"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🎨 Pinterest-Style Features:"
echo "   📱 Masonry grid layout"
echo "   🔄 Infinite scroll"
echo "   📲 Pull-to-refresh (mobile)"
echo "   🎭 Hover overlays"
echo "   📤 Image upload"
echo "   🔍 Real-time search"
echo ""
echo "📚 Documentation:"
echo "   📖 README.md"
echo "   🎨 PINTEREST_INTERFACE_GUIDE.md"
echo "   🔧 SUPABASE_SETUP.md"
echo ""
echo "🎉 Enjoy your Pinterest-style inventory management!"
