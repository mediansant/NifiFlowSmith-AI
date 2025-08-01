#!/bin/bash

echo "📊 NiFi Status Check"
echo "==================="

# Check if container is running
if docker ps | grep -q nifi-local; then
    echo "✅ NiFi container is running"
    
    # Check container status
    echo ""
    echo "📋 Container Details:"
    docker ps --filter name=nifi-local --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
    # Check if NiFi web UI is accessible
    echo ""
    echo "🌐 Web UI Check:"
    if curl -s http://localhost:8080/nifi > /dev/null 2>&1; then
        echo "✅ NiFi Web UI is accessible at http://localhost:8080/nifi"
    else
        echo "❌ NiFi Web UI is not accessible"
    fi
    
    # Check if NiFi REST API is accessible
    echo ""
    echo "🔧 REST API Check:"
    if curl -u admin:admin123 -s http://localhost:8080/nifi-api/process-groups/root > /dev/null 2>&1; then
        echo "✅ NiFi REST API is accessible at http://localhost:8080/nifi-api"
    else
        echo "❌ NiFi REST API is not accessible"
    fi
    
else
    echo "❌ NiFi container is not running"
    echo ""
    echo "To start NiFi: ./scripts/start-nifi.sh"
fi 