# Bodai Component Roles

This document provides detailed descriptions of each component in the Bodai ecosystem, including their responsibilities, port assignments, and relationships.

## Component Overview

The Bodai ecosystem consists of six components, each with a distinct role derived from Sanskrit terminology (core) or functional descriptions representing their function in the system.

______________________________________________________________________

## Mahavishnu - The Orchestrator

| Attribute | Value |
|-----------|-------|
| **Port** | 8680 |
| **Role** | Multi-engine workflow orchestration |
| **Etymology** | Sanskrit *maha* (great) + *Vishnu* (the preserver in Hindu trinity) |

### Responsibilities

- Route tasks to appropriate execution engines
- Manage workflow definitions and templates
- Coordinate multi-step processes across components
- Handle task queuing and prioritization
- Provide workflow status monitoring
- Support multiple execution backends (local, docker, cloud)
- Enable workflow composition and chaining
- Manage workflow versioning and rollback

### Key Interactions

- Sends tasks to **Akosha** for intelligence operations
- Persists state to **Druva** for recovery
- Tracks context in **Session-Buddy**
- Validates with **Crackerjack** before execution

______________________________________________________________________

## Akosha - The Seer

| Attribute | Value |
|-----------|-------|
| **Port** | 8682 |
| **Role** | Cross-system intelligence, vector embeddings |
| **Etymology** | Sanskrit *akasha* (sky, ether, space) - the fifth element, medium of consciousness |

### Responsibilities

- Generate and manage vector embeddings
- Provide semantic search capabilities
- Detect patterns across system data
- Enable cross-session intelligence
- Support similarity queries
- Maintain knowledge graphs
- Provide recommendation engines
- Enable predictive analysis

### Key Interactions

- Receives session data from **Session-Buddy**
- Stores patterns in **Druva**
- Provides intelligence to **Mahavishnu**
- Receives code analysis from **Crackerjack**

______________________________________________________________________

## Druva - The Curator

| Attribute | Value |
|-----------|-------|
| **Port** | 8683 |
| **Role** | Persistent object storage with ACID |
| **Etymology** | Sanskrit *druva* (firm, constant, unchanging) - also the Pole Star |

### Responsibilities

- Provide persistent object storage
- Ensure ACID transaction guarantees
- Manage data versioning and history
- Handle data migration and backup
- Support efficient querying and indexing
- Enable data recovery and restore
- Manage storage quotas and cleanup
- Provide data integrity verification

### Key Interactions

- Stores state for **Mahavishnu**
- Persists patterns for **Akosha**
- Backs up sessions for **Session-Buddy**
- Stores quality reports for **Crackerjack**

______________________________________________________________________

## Session-Buddy - The Builder

| Attribute | Value |
|-----------|-------|
| **Port** | 8678 |
| **Role** | Session lifecycle, knowledge graphs |
| **Sanskrit Meaning** | Not Sanskrit - named for its function as a companion |

### Responsibilities

- Manage session lifecycle (create, update, close)
- Track conversation history and context
- Build and maintain knowledge graphs
- Provide session recovery capabilities
- Enable context switching between sessions
- Support session sharing and collaboration
- Track session metrics and analytics
- Manage session permissions and access

### Key Interactions

- Sends data to **Akosha** for embedding
- Stores backups in **Druva**
- Provides context to **Mahavishnu**
- Receives quality metrics from **Crackerjack**

______________________________________________________________________

## Crackerjack - The Inspector

| Attribute | Value |
|-----------|-------|
| **Port** | 8676 |
| **Role** | Quality gates, testing, CI/CD |
| **Sanskrit Meaning** | Not Sanskrit - named for excellence and precision |

### Responsibilities

- Enforce quality gates across the ecosystem
- Run automated test suites
- Manage CI/CD pipelines
- Provide code analysis and linting
- Track quality metrics over time
- Enable quality reporting and dashboards
- Support custom quality rules
- Integrate with external quality services

### Key Interactions

- Validates workflows for **Mahavishnu**
- Sends code analysis to **Akosha**
- Stores reports in **Druva**
- Records metrics in **Session-Buddy**

______________________________________________________________________

## Oneiric - The Resolver

| Attribute | Value |
|-----------|-------|
| **Port** | N/A (Library only) |
| **Role** | Conflict resolution, dependency analysis |
| **Etymology** | Greek *oneiros* (dream) - relating to dreams, the abstract and complex |

### Responsibilities

- Provide conflict resolution algorithms
- Analyze dependency graphs
- Detect and resolve version conflicts
- Support merge strategies
- Enable dependency optimization
- Provide resolution suggestions
- Support constraint satisfaction
- Enable what-if analysis

### Key Characteristics

- **No MCP Server**: Absorbed into Druva for persistence operations
- **Library Only**: Functions as a shared library, not a network service
- **Stateless**: Does not maintain runtime state
- **Embedded**: Used directly by other components

### Key Interactions

- Used by **Mahavishnu** for workflow conflict resolution
- Used by **Druva** for data merge operations
- Used by **Session-Buddy** for context merging

______________________________________________________________________

## Role Summary Table

| Component | Port | Role Type | Stateful | Network Service | License |
|-----------|------|-----------|----------|-----------------|---------|
| Mahavishnu | 8680 | Orchestrator | No | Yes | BSD-3 |
| Akosha | 8682 | Intelligence | Yes | Yes | BSD-3 |
| Druva | 8683 | Storage | Yes | Yes | BSD-3 |
| Session-Buddy | 8678 | Session Manager | Yes | Yes | BSD-3 |
| Crackerjack | 8676 | Quality Enforcer | No | Yes | BSD-3 |
| Oneiric | N/A | Foundation Library | No | No | BSD-3 |

## Related Documentation

- [Architecture](architecture.md) - System overview and data flow
- [Symbiosis](symbiosis.md) - How components work together
- [Port Map](portmap.md) - Port allocation and rationale
