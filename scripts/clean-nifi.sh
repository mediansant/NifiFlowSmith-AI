#!/bin/bash

echo "🧹 Cleaning NiFi data..."

# Stop containers
docker-compose down

# Remove volumes
docker-compose down -v

echo "✅ NiFi data cleaned!"
echo ""
echo "To start fresh: ./scripts/start-nifi.sh" 