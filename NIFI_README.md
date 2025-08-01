# NiFi Local Development Setup

A simple vanilla NiFi Docker setup for the NiFi NL Builder project.

## Quick Start

```bash
# Start NiFi
./scripts/start-nifi.sh

# Check status
./scripts/check-nifi.sh

# Stop NiFi
./scripts/stop-nifi.sh

# Clean all data
./scripts/clean-nifi.sh
```

## Access Points

- **NiFi Web UI**: http://localhost:8080/nifi
- **NiFi REST API**: http://localhost:8080/nifi-api
- **Username**: admin
- **Password**: admin123

## Configuration

The NiFi instance is configured with:
- Single-user authentication (admin/admin123)
- HTTP access (no HTTPS)
- Standalone mode (no clustering)
- Persistent data storage via Docker volumes

## Environment Variables

Update your `.env` file with:
```bash
NIFI_URL=http://localhost:8080
NIFI_USERNAME=admin
NIFI_PASSWORD=admin123
```

## Troubleshooting

1. **NiFi not starting**: Check Docker is running
2. **Can't access web UI**: Wait a few minutes for startup
3. **REST API issues**: Verify port 8080 is not in use
4. **Permission errors**: Run `chmod +x scripts/*.sh`

## Data Persistence

NiFi data is stored in Docker volumes:
- `nifi_database_repository`: Database files
- `nifi_flowfile_repository`: FlowFile data
- `nifi_content_repository`: Content storage
- `nifi_provenance_repository`: Provenance data
- `nifi_state`: State information
- `nifi_logs`: Log files
- `nifi_conf`: Configuration files

To completely reset: `./scripts/clean-nifi.sh` 