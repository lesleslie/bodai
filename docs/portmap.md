# Bodai Port Map

This document describes the port allocation for the Bodai ecosystem, including the rationale for the chosen range and guidelines for future allocations.

## Port Allocation

The Bodai ecosystem uses ports in the 8676-8699 range, providing a dedicated namespace for ecosystem services.

| Port | Component | Role | Status |
|------|-----------|------|--------|
| 8676 | Crackerjack | Inspector | Active |
| 8677 | - | Reserved | Available |
| 8678 | Session-Buddy | Builder | Active |
| 8679 | - | Reserved | Available |
| 8680 | Mahavishnu | Orchestrator | Active |
| 8681 | - | Reserved (Oneiric) | See Note |
| 8682 | Akosha | Seer | Active |
| 8683 | Dhruva | Curator | Active |
| 8684-8699 | - | Reserved | Available |

### Port 8681 Note

Port 8681 is reserved for historical consistency. Oneiric was originally planned as a network service but was absorbed into Dhruva as a library component. The port remains reserved to:

- Prevent accidental allocation
- Maintain consistent port spacing
- Allow for potential future use
- Avoid confusion with existing documentation

## Port Range Rationale

### Why 8676-8699?

The 8676-8699 range was chosen for several reasons:

1. **Unallocated Range**: This range falls within the dynamic/private port range (49152-65535) but is not commonly used by well-known services, reducing collision risk.

2. **Memorable Pattern**: The 86xx pattern is easy to remember and type:
   - 8676 = Crackerjack (starts with 6 for "Crackerjack" alphabet position)
   - 8678 = Session-Buddy (8 for "Buddy")
   - 8680 = Mahavishnu (0 for "Orchestrator" - central hub)
   - 8682 = Akosha (2 for "Seer" - second eye)
   - 8683 = Dhruva (3 for "Curator" - third pillar)

3. **Grouped Allocation**: All Bodai services are in one contiguous range, making firewall rules and network configuration simpler.

4. **Future Growth**: 24 ports (8676-8699) provide ample room for expansion.

### Port Assignment Strategy

Within the range, ports are assigned based on:

| Component Type | Port Pattern | Examples |
|----------------|--------------|----------|
| Infrastructure | 867x | Crackerjack (8676), Session-Buddy (8678) |
| Core Services | 868x | Mahavishnu (8680), Akosha (8682), Dhruva (8683) |
| Future Expansion | 869x | Available |

## Current Allocation Detail

### Crackerjack (8676)

```
Port: 8676
Service: Crackerjack Inspector
Protocol: HTTP/WebSocket
Endpoints:
  - /health - Health check
  - /run - Execute quality checks
  - /report - Quality report generation
  - /watch - File watcher for continuous checks
```

### Session-Buddy (8678)

```
Port: 8678
Service: Session-Buddy Builder
Protocol: HTTP/WebSocket
Endpoints:
  - /health - Health check
  - /session - Session management
  - /context - Context retrieval
  - /knowledge - Knowledge graph operations
```

### Mahavishnu (8680)

```
Port: 8680
Service: Mahavishnu Orchestrator
Protocol: HTTP/WebSocket/gRPC
Endpoints:
  - /health - Health check
  - /workflow - Workflow management
  - /execute - Task execution
  - /status - Workflow status
```

### Akosha (8682)

```
Port: 8682
Service: Akosha Seer
Protocol: HTTP/WebSocket
Endpoints:
  - /health - Health check
  - /embed - Generate embeddings
  - /search - Semantic search
  - /patterns - Pattern detection
```

### Dhruva (8683)

```
Port: 8683
Service: Dhruva Curator
Protocol: HTTP/WebSocket
Endpoints:
  - /health - Health check
  - /store - Object storage
  - /query - Query interface
  - /backup - Backup operations
```

## Network Configuration

### Local Development

For local development, all services bind to localhost:

```yaml
# Bodai ecosystem local configuration
services:
  crackerjack:
    host: localhost
    port: 8676

  session-buddy:
    host: localhost
    port: 8678

  mahavishnu:
    host: localhost
    port: 8680

  akosha:
    host: localhost
    port: 8682

  dhruva:
    host: localhost
    port: 8683
```

### Docker Deployment

When deployed via Docker, services use internal networking:

```yaml
# docker-compose.yml example
services:
  crackerjack:
    ports:
      - "8676:8676"

  session-buddy:
    ports:
      - "8678:8678"

  mahavishnu:
    ports:
      - "8680:8680"

  akosha:
    ports:
      - "8682:8682"

  dhruva:
    ports:
      - "8683:8683"
```

### Firewall Rules

To allow Bodai ecosystem traffic:

```bash
# Allow all Bodai ports
sudo ufw allow 8676:8699/tcp

# Or allow specific ports
sudo ufw allow 8676/tcp comment 'Crackerjack'
sudo ufw allow 8678/tcp comment 'Session-Buddy'
sudo ufw allow 8680/tcp comment 'Mahavishnu'
sudo ufw allow 8682/tcp comment 'Akosha'
sudo ufw allow 8683/tcp comment 'Dhruva'
```

## Health Check Endpoints

All services provide a `/health` endpoint on their assigned port:

| Service | Port | Health Check URL |
|---------|------|------------------|
| Crackerjack | 8676 | `http://localhost:8676/health` |
| Session-Buddy | 8678 | `http://localhost:8678/health` |
| Mahavishnu | 8680 | `http://localhost:8680/health` |
| Akosha | 8682 | `http://localhost:8682/health` |
| Dhruva | 8683 | `http://localhost:8683/health` |

### Health Check Response Format

All services return a consistent health check response:

```json
{
  "status": "healthy",
  "service": "service-name",
  "version": "x.y.z",
  "uptime_seconds": 12345,
  "dependencies": {
    "dependency_name": "healthy"
  }
}
```

## Port Conflict Resolution

If a port is already in use:

1. **Check what's using the port**:
   ```bash
   lsof -i :8676
   ```

2. **Kill the conflicting process** (if appropriate):
   ```bash
   kill -9 <PID>
   ```

3. **Or reconfigure the service** (not recommended - breaks ecosystem consistency):
   ```yaml
   # Only as a last resort
   services:
     crackerjack:
       port: 9676  # Alternate port
   ```

## Future Allocation Guidelines

When adding new services to the ecosystem:

1. **Use 867x for infrastructure tools** (testing, monitoring, etc.)
2. **Use 868x for core services** (storage, intelligence, orchestration)
3. **Use 869x for extensions** (plugins, external integrations)
4. **Always check this document first** to avoid conflicts
5. **Update this document** when allocating a new port
6. **Reserve adjacent ports** if a service might need multiple ports

## Related Documentation

- [Architecture](architecture.md) - System overview and data flow
- [Roles](roles.md) - Detailed descriptions of each component
- [Symbiosis](symbiosis.md) - How components work together
