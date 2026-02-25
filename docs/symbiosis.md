# Bodai Symbiosis

This document describes how the components in the Bodai ecosystem work together, forming a symbiotic relationship where each component enhances the capabilities of others.

## Overview

The Bodai ecosystem is designed around the principle of symbiosis - components are not merely connected, but actively enhance each other's capabilities through well-defined interactions.

______________________________________________________________________

## Session-Buddy to Akosha

### The Memory-Intelligence Pipeline

Session-Buddy captures the ephemeral (sessions, conversations) and feeds them to Akosha, which transforms them into the persistent (embeddings, patterns).

```
+-------------------+          +-------------------+
|   Session-Buddy   |          |      Akosha       |
|     (Builder)     |          |      (Seer)       |
+-------------------+          +-------------------+
|                   |          |                   |
| Sessions   ------>+--------->+ Vector Store      |
| Conversations ----+--------->+ Embeddings        |
| Context    ------>+--------->+ Patterns          |
| Knowledge  ------>+--------->+ Intelligence      |
|                   |          |                   |
+-------------------+          +-------------------+
        :8678                         :8682
```

### Data Flow Details

1. **Session Creation**: When a new session starts in Session-Buddy
1. **Context Capture**: Conversation and context are captured
1. **Embedding Generation**: Akosha generates vector embeddings
1. **Pattern Detection**: Cross-session patterns are identified
1. **Intelligence Retrieval**: Future sessions can query related context

### Symbiotic Benefits

| Session-Buddy Provides | Akosha Provides |
|------------------------|-----------------|
| Raw session data | Semantic search |
| Conversation history | Pattern recognition |
| Context windows | Intelligent retrieval |
| Knowledge graph nodes | Cross-session intelligence |

______________________________________________________________________

## Mahavishnu to All Components

### The Orchestrator's Reach

Mahavishnu orchestrates workflows across all components, acting as the central nervous system of the ecosystem.

```
                         +-------------------+
                         |    Mahavishnu     |
                         |   (Orchestrator)  |
                         +-------------------+
                         |                   |
                         |  Workflow Engine  |
                         |  Task Router      |
                         |  State Manager    |
                         |                   |
                         +---------+---------+
                                   |
          +------------------------+------------------------+
          |                        |                        |
          v                        v                        v
    +-----------+           +-----------+           +-----------+
    |   Akosha  |           |   Druva  |           | Session-  |
    |  (Seer)   |           | (Curator) |           |  Buddy    |
    +-----------+           +-----------+           +-----------+
    | Intelligence|         | Persistence|         | Sessions  |
    | Patterns    |         | State      |         | Context   |
    | Search      |         | Recovery   |         | History   |
    +-----------+           +-----------+           +-----------+
          :8682                   :8683                  :8678

          +------------------------+
          |
          v
    +-----------+
    | Crackerjack|
    | (Inspector)|
    +-----------+
    | Quality   |
    | Testing   |
    | CI/CD     |
    +-----------+
          :8676
```

### Orchestration Patterns

#### Intelligence Query Pattern

```
Mahavishnu --[query]--> Akosha --[results]--> Mahavishnu
```

Used when a workflow needs semantic search or pattern matching.

#### State Persistence Pattern

```
Mahavishnu --[state]--> Druva --[confirm]--> Mahavishnu
```

Used for checkpointing workflow progress.

#### Session Context Pattern

```
Mahavishnu --[context_request]--> Session-Buddy --[context]--> Mahavishnu
```

Used for context-aware workflow execution.

#### Quality Validation Pattern

```
Mahavishnu --[artifact]--> Crackerjack --[quality_report]--> Mahavishnu
```

Used for quality gate enforcement.

### Symbiotic Benefits

| To Component | Mahavishnu Provides | Component Provides |
|--------------|---------------------|-------------------|
| Akosha | Query orchestration | Intelligence results |
| Druva | State to persist | Recovery capability |
| Session-Buddy | Context requests | Session awareness |
| Crackerjack | Artifacts to validate | Quality assurance |

______________________________________________________________________

## Crackerjack to All Components

### The Inspector's Watch

Crackerjack enforces quality across the entire ecosystem, ensuring that all components operate at the required standard.

```
                         +-------------------+
                         |    Crackerjack    |
                         |    (Inspector)    |
                         +-------------------+
                         |                   |
                         |  Quality Gates    |
                         |  Test Runner      |
                         |  CI/CD Pipeline   |
                         |  Code Analysis    |
                         |                   |
                         +---------+---------+
                                   |
          +------------------------+------------------------+
          |             |            |            |         |
          v             v            v            v         v
    +---------+   +---------+  +---------+  +---------+  +---------+
    |Mahavishnu|  | Akosha  |  | Druva  |  |Session- |  | Oneiric |
    |          |  |         |  |         |  | Buddy   |  | (lib)   |
    +---------+   +---------+  +---------+  +---------+  +---------+
         :8680        :8682        :8683        :8678       N/A
```

### Quality Enforcement Points

#### Workflow Quality (Mahavishnu)

```
+-------------+     +-------------+     +-------------+
|  Workflow   |---->| Crackerjack |---->| Validated   |
|  Definition |     | Validation  |     | Workflow    |
+-------------+     +-------------+     +-------------+
```

#### Code Analysis Embeddings (Akosha)

```
+-------------+     +-------------+     +-------------+
| Source Code |---->| Crackerjack |---->| Akosha      |
|             |     | Analysis    |     | Embeddings  |
+-------------+     +-------------+     +-------------+
```

#### Quality Report Storage (Druva)

```
+-------------+     +-------------+     +-------------+
| Quality Run |---->| Crackerjack |---->| Druva      |
|             |     | Report Gen  |     | Storage     |
+-------------+     +-------------+     +-------------+
```

#### Session Quality Metrics (Session-Buddy)

```
+-------------+     +-------------+     +-------------+
| Session End |---->| Crackerjack |---->| Session     |
|             |     | Metrics     |     | Quality Log |
+-------------+     +-------------+     +-------------+
```

### Symbiotic Benefits

| To Component | Crackerjack Provides | Component Provides |
|--------------|---------------------|-------------------|
| Mahavishnu | Workflow validation | Workflows to validate |
| Akosha | Code embeddings | Search capability |
| Druva | Quality reports | Persistent storage |
| Session-Buddy | Quality metrics | Session context |
| Oneiric | Library validation | Resolution logic |

______________________________________________________________________

## Druva to All Components

### The Curator's Archive

Druva provides the persistent foundation for the entire ecosystem, ensuring data survives across sessions, restarts, and failures.

```
                         +-------------------+
                         |      Druva       |
                         |     (Curator)     |
                         +-------------------+
                         |                   |
                         |  Object Storage   |
                         |  ACID Transactions|
                         |  Version Control  |
                         |  Backup/Recovery  |
                         |                   |
                         +---------+---------+
                                   |
          +------------------------+------------------------+
          |             |            |            |         |
          v             v            v            v         v
    +---------+   +---------+  +---------+  +---------+  +---------+
    |Mahavishnu|  | Akosha  |  |Session- |  |Cracker- |  | Oneiric |
    |          |  |         |  | Buddy   |  | jack    |  | (lib)   |
    +---------+   +---------+  +---------+  +---------+  +---------+
         :8680        :8682        :8678        :8676       N/A
```

### Storage Services

#### Workflow State Recovery (Mahavishnu)

```
Mahavishnu                      Druva
    |                              |
    +--[checkpoint state]--------->|
    |                              |
    +--[failure occurs]            |
    |                              |
    +--[request recovery]--------->|
    |<--[restored state]-----------|
    |                              |
```

#### Historical Pattern Data (Akosha)

```
Akosha                          Druva
    |                              |
    +--[new pattern found]-------->|
    |                              |
    +--[query history]------------>|
    |<--[historical patterns]------|
    |                              |
```

#### Session Backup (Session-Buddy)

```
Session-Buddy                   Druva
    |                              |
    +--[session data]------------->|
    |                              |
    +--[disaster occurs]           |
    |                              |
    +--[request restore]---------->|
    |<--[recovered sessions]-------|
    |                              |
```

#### Quality Trend Data (Crackerjack)

```
Crackerjack                     Druva
    |                              |
    +--[quality report]----------->|
    |                              |
    +--[query trends]------------->|
    |<--[historical trends]--------|
    |                              |
```

### Symbiotic Benefits

| To Component | Druva Provides | Component Provides |
|--------------|-----------------|-------------------|
| Mahavishnu | State recovery | Checkpoint data |
| Akosha | Historical data | Patterns to store |
| Session-Buddy | Disaster recovery | Sessions to backup |
| Crackerjack | Trend analysis | Reports to store |
| Oneiric | Merge resolution data | Resolution algorithms |

______________________________________________________________________

## Oneiric to All Components

### The Resolver's Logic

Oneiric is unique in the ecosystem - it is a library, not a service. This design choice was intentional: resolution algorithms are CPU-bound and benefit from direct function calls rather than network round-trips.

```
+-------------------+
|      Oneiric      |
|     (Resolver)    |
+-------------------+
|                   |
| Conflict Resolution
| Dependency Analysis
| Merge Strategies  |
| Constraint Solving|
|                   |
+-------------------+
         |
         | Direct Function Calls (No Network)
         |
    +----+----+----+----+
    |    |    |    |    |
    v    v    v    v    v
 +-----+-----+-----+-----+
 |Maha |Akosh|Dhruv|Sessn|
 |vishnu| a  |  a  |Buddy|
 +-----+-----+-----+-----+
```

### Library Integration Points

#### Workflow Conflict Resolution (Mahavishnu)

```python
# Mahavishnu uses Oneiric directly
from oneiric import resolve_workflow_conflict

result = resolve_workflow_conflict(
    local_workflow,
    remote_workflow,
    strategy="three_way_merge"
)
```

#### Data Merge Operations (Druva)

```python
# Druva uses Oneiric for data merges
from oneiric import merge_objects

merged = merge_objects(
    base=base_version,
    ours=local_changes,
    theirs=remote_changes
)
```

#### Context Merging (Session-Buddy)

```python
# Session-Buddy uses Oneiric for context merging
from oneiric import merge_contexts

unified_context = merge_contexts(
    contexts=[session_a, session_b],
    priority="most_recent"
)
```

### Symbiotic Benefits

| Component | Uses Oneiric For | Benefit |
|-----------|------------------|---------|
| Mahavishnu | Workflow conflict resolution | No workflow data loss |
| Druva | Data merge operations | ACID-safe merges |
| Session-Buddy | Context merging | Unified session view |
| Crackerjack | Rule conflict resolution | Consistent quality rules |
| Akosha | Pattern conflict resolution | Accurate pattern matching |

______________________________________________________________________

## The Complete Symbiosis

When all components work together, the ecosystem achieves capabilities beyond what any single component could provide:

```
                    +---------------------------+
                    |         BODAI             |
                    |       (The Orb)           |
                    |  Meta-Project / Config    |
                    +---------------------------+
                                |
         +----------------------+----------------------+
         |                      |                      |
         v                      v                      v
+----------------+    +----------------+    +----------------+
|  Crackerjack   |    |  Mahavishnu    |    | Session-Buddy  |
|  (Inspector)   |    |  (Orchestrator)|    |   (Builder)    |
|    :8676       |    |     :8680      |    |     :8678      |
+----------------+    +----------------+    +----------------+
         |                      |                      |
         |                      |                      |
         |    +-----------------+-----------------+    |
         |    |                                   |    |
         v    v                                   v    v
    +----------------+                   +----------------+
    |     Druva     |<----------------->|     Akosha     |
    |    (Curator)   |                   |     (Seer)     |
    |      :8683     |                   |      :8682     |
    +----------------+                   +----------------+
              ^                                    ^
              |                                    |
              +------------------------------------+
                              |
                    +-------------------+
                    |      Oneiric      |
                    | (Resolver Library)|
                    +-------------------+
```

### Emergent Capabilities

| Capability | Components Involved |
|------------|-------------------|
| Intelligent Workflows | Mahavishnu + Akosha + Session-Buddy |
| Quality-Assured Intelligence | Crackerjack + Akosha + Druva |
| Resilient Sessions | Session-Buddy + Druva + Oneiric |
| Self-Improving Quality | Crackerjack + Akosha + Druva |
| Cross-Component Recovery | Druva + Oneiric + All |

## Related Documentation

- [Architecture](architecture.md) - System overview and data flow
- [Roles](roles.md) - Detailed descriptions of each component
- [Port Map](portmap.md) - Port allocation and rationale
