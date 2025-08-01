#!/bin/bash

echo "🚀 Starting NiFi..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start NiFi
docker-compose up -d

echo "⏳ Waiting for NiFi to start..."
until curl -s http://localhost:8080/nifi > /dev/null 2>&1; do
    echo "   Waiting for NiFi web interface..."
    sleep 15
done

echo "✅ NiFi is ready!"
echo ""
echo "🌐 NiFi Web UI: http://localhost:8080/nifi"
echo "🔧 NiFi REST API: http://localhost:8080/nifi-api"
echo "👤 Username: admin"
echo "🔑 Password: admin123"
echo ""
echo "📊 Check status: ./scripts/check-nifi.sh"
echo "🛑 Stop NiFi: ./scripts/stop-nifi.sh"
