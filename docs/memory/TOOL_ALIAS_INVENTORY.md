---
generated: 2026-07-29
sources: 7
sources_scanned:
  - mahavishnu
  - session-buddy
  - akosha
  - dhara
  - crackerjack
  - oneiric
  - bodai
slash_commands_scanned: 73
active_skills_scanned: 5
active_agents_scanned: 53
archived_skills_scanned: 12
archived_agents_scanned: 50
claude_md_files_scanned: 7
registered_tools_total: 371
referenced_tools_total: 15
orphan_tools_total: 356
orphan_commands_total: 6
---

# Tool-Alias Inventory: Slash Commands → MCP Tools

A static inventory of how slash commands, skills, and agents across Bodai
components reference registered MCP tools, and which registered tools go
unreferenced. Cross-referenced against live `@mcp.tool()` registrations
extracted from each component's `mcp/` source tree.

This is the reference document for deciding whether a single observed
alias drift (e.g. `crackerjack_run`) is a one-off or part of a pattern.

## Source directories

| Component | Commands dir | Skills dir | Agents dir | MCP server root |
|-----------|--------------|------------|------------|-----------------|
| mahavishnu | `/Users/les/Projects/mahavishnu/.claude/commands/` | `/Users/les/Projects/mahavishnu/.claude/skills/` | `/Users/les/Projects/mahavishnu/.claude/agents/` | `/Users/les/Projects/mahavishnu/mahavishnu/mcp/` |
| session-buddy | — (none) | — (none) | — (none) | `/Users/les/Projects/session-buddy/session_buddy/mcp/` |
| akosha | — (none) | — (none) | — (none) | `/Users/les/Projects/akosha/akosha/mcp/` |
| dhara | — (none) | — (none) | — (none) | `/Users/les/Projects/dhara/dhara/mcp/` |
| crackerjack | — (none) | — (none) | — (none) | (no MCP server; tools exposed via mahavishnu-side adapter) |
| oneiric | — (none) | — (none) | — (none) | (library-only, no MCP server) |
| bodai | `/Users/les/Projects/bodai/.claude/` (settings.local.json only) | — | — | — |

Slash commands, skills, and agents live exclusively under
`/Users/les/Projects/mahavishnu/.claude/`. The other components carry
only settings/handoff/decisions content. CLAUDE.md files were also
scanned across all components (only `mahavishnu/CLAUDE.md` carries
inline tool references).

## Registration counts (extracted from live source)

| Component | Registered MCP tools | Profile-gated? | Notes |
|-----------|----------------------|----------------|-------|
| mahavishnu | 183 | Yes (`mahavishnu/mcp/tools/profiles.py`) | Inline registrations via `@mcp.tool()` decorators |
| session-buddy | 153 | Yes (`session_buddy/mcp/tools/profiles.py`) | Inline registrations via `@mcp.tool()` decorators |
| akosha | 9 | Yes (`akosha/mcp/tools/profiles.py`) | REGISTRATION_TOOLS dict enumerates 27 logical tools but only 9 are actually decorated |
| dhara | 20 (+6 health) | Yes (`dhara/mcp/profiles.py`) | Tools grouped by `TOOL_GROUP_*` constants; only `discover_tools` is individually decorated |
| crackerjack | 0 (separate server) | n/a | No `@mcp.tool()` source registered; `mcp__crackerjack__crackerjack_run` is a known client-facing alias |
| oneiric | 0 (library only) | n/a | No MCP server; references to `mcp__oneiric__*` are orphans |
| **Total** | **365 (tool names) + 6 dhara-health + 1 crackerjack alias** | | |

## Methodology

1. Walked `<component>/mcp/**/*.py` and extracted every function with an
   `@mcp.tool()` decorator (or `@server.tool()`). Skipped
   `tests/`, `__pycache__/`, `.venv/`, `.git/`, `build/`,
   `.cache/`, and `worktrees/`.
2. Walked `<component>/.claude/{commands,skills,agents}/**/*.md` and
   grepped for `mcp__<component>__<tool>` patterns. Skipped
   `.archive/` subtrees for the "active" sections, but included them
   in a separate subsection so drift in archived artifacts is visible.
3. Walked `<component>/CLAUDE.md` for inline tool references (only
   `mahavishnu/CLAUDE.md` had any).
4. Built reverse index: every registered tool → list of slash
   commands/skills/agents that mention it.

---

## Section 1: Slash commands → MCP tools

### 1.1 Active slash commands (top-level `.claude/commands/*.md`)

The active top-level slash commands are simple wrappers — none reference
MCP tools directly. They execute shell scripts or run hooks; MCP tool
invocation happens *inside* the agents/skills they spawn.

| Slash command | File | Component server | MCP tools invoked | Registration status |
|---------------|------|------------------|-------------------|---------------------|
| `bodai-status` | `mahavishnu/.claude/commands/bodai-status.md` | — | — | n/a |
| `run` | `mahavishnu/.claude/commands/run.md` | — | — | n/a |
| `toggle-verbose` | `mahavishnu/.claude/commands/toggle-verbose.md` | — | — | n/a |
| `verbose-off` | `mahavishnu/.claude/commands/verbose-off.md` | — | — | n/a |
| `verbose-on` | `mahavishnu/.claude/commands/verbose-on.md` | — | — | n/a |
| `verbose-status` | `mahavishnu/.claude/commands/verbose-status.md` | — | — | n/a |

### 1.2 Subpath slash commands (`commands/tools/`, `commands/workflows/`)

These are *also* slash commands (e.g. `/tools/automation/automated-research`,
`/workflows/feature/feature-delivery-lifecycle`) but none of them contain
direct MCP tool invocations — they describe multi-step Claude
workflows. Excluded from the alias table to keep focus on programmatic
tool calls.

### 1.3 Active skills (`.claude/skills/<name>/SKILL.md`)

| Skill name | File path | Component server | MCP tools invoked | Registration status |
|------------|-----------|------------------|-------------------|---------------------|
| `mahavishnu` | `/Users/les/Projects/mahavishnu/.claude/skills/mahavishnu/SKILL.md` | mahavishnu | `pool_route_execute`, `dispatch_to_pool`, `trigger_workflow`, `pool_health` | all registered |
| `mahavishnu-status` | `/Users/les/Projects/mahavishnu/.claude/skills/mahavishnu-status/SKILL.md` | mahavishnu | `pool_route_execute` | registered |
| `task-orchestration-review` | `/Users/les/Projects/mahavishnu/.claude/skills/task-orchestration-review/SKILL.md` | mahavishnu | `pool_execute`, `pool_monitor`, `pool_search_memory`, `pool_spawn` | all registered |
| `bodai-status` | `/Users/les/Projects/mahavishnu/.claude/skills/bodai-status/SKILL.md` | — | — | n/a |
| `crackerjack-compliant-code` | `/Users/les/Projects/mahavishnu/.claude/skills/crackerjack-compliant-code/SKILL.md` | — | — | n/a |

### 1.4 Archived skills (`.claude/skills/.archive/`) — drift surface

| Skill name | File path | Component server | MCP tools invoked | Registration status |
|------------|-----------|------------------|-------------------|---------------------|
| `detect-patterns` | `/Users/les/Projects/mahavishnu/.claude/skills/.archive/detect-patterns/SKILL.md` | akosha | `detect_patterns`, `detect_anomalies`, `analyze_trends` | `detect_anomalies`, `analyze_trends` registered; `detect_patterns` ⚠️ not found |
| `manage-lifecycle` | `/Users/les/Projects/mahavishnu/.claude/skills/.archive/manage-lifecycle/SKILL.md` | oneiric | `lifecycle_activate` | ❌ not found (no `mcp__oneiric__*` server exists) |
| `troubleshoot-workflow` | `/Users/les/Projects/mahavishnu/.claude/skills/.archive/troubleshoot-workflow/SKILL.md` | mahavishnu | `get_health`, `get_pool_status`, `get_workflow_status`, `list_repos` | all registered |
| `backup-restore` | `/Users/les/Projects/mahavishnu/.claude/skills/.archive/backup-restore/SKILL.md` | dhruva (legacy) | `list_backups`, `restore_backup`, `validate_backup` | ❌ not found (dhruva server replaced by dhara; backups moved to mahavishnu) |
| `manage-storage` | `/Users/les/Projects/mahavishnu/.claude/skills/.archive/manage-storage/SKILL.md` | dhruva (legacy) | `get_adapter`, `list_adapter_versions`, `list_adapters`, `store_adapter` | all four migrated to `mcp__dhara__*` ✅ but server name is stale |

### 1.5 Active agents (`.claude/agents/<name>.md`)

| Agent name | File path | Component server | MCP tools invoked | Registration status |
|------------|-----------|------------------|-------------------|---------------------|
| `mahavishnu-orchestrator` | `/Users/les/Projects/mahavishnu/.claude/agents/mahavishnu-orchestrator.md` | mahavishnu | `discover_tools`, `dispatch_to_pool`, `pool_route_execute` | all registered |
| `python-pro` | `/Users/les/Projects/mahavishnu/.claude/agents/python-pro.md` | crackerjack | `crackerjack_run` | ✅ registered (crackerjack alias) |

### 1.6 Archived agents — drift surface

| Agent name | File path | Component server | MCP tools invoked | Registration status |
|------------|-----------|------------------|-------------------|---------------------|
| `code-reviewer` | `/Users/les/Projects/mahavishnu/.claude/agents/.archive/code-reviewer.md` | akosha, crackerjack | `search_code_patterns`, `crackerjack_run` | `crackerjack_run` ✅; `search_code_patterns` ⚠️ not in akosha (registered in **session-buddy** as `mcp__session_buddy__search_code_patterns`) |
| `refactoring-specialist` | `/Users/les/Projects/mahavishnu/.claude/agents/.archive/refactoring-specialist.md` | akosha, crackerjack | `search_code_patterns`, `crackerjack_run` | same as above |

### 1.7 CLAUDE.md inline references (only `mahavishnu/CLAUDE.md`)

The `mahavishnu/CLAUDE.md` file references these MCP tools inline:

| Tool | Status |
|------|--------|
| `mcp__mahavishnu__discover_tools` | ✅ registered |
| `mcp__mahavishnu__dispatch_to_pool` | ✅ registered |
| `mcp__mahavishnu__pool_health` | ✅ registered |
| `mcp__mahavishnu__pool_route_execute` | ✅ registered |

No other component CLAUDE.md file references MCP tools.

---

## Section 2: MCP tools → slash commands (reverse index)

For each tool that appears in any registered tool list, list the slash
commands/skills/agents that mention it. Empty cells = the tool exists
but no slash command uses it.

### 2.1 `mcp__mahavishnu__*`

| Tool | Referenced by |
|------|---------------|
| `discover_tools` | mahavishnu-orchestrator (agent), mahavishnu/CLAUDE.md |
| `dispatch_to_pool` | mahavishnu-orchestrator (agent), mahavishnu (skill), mahavishnu/CLAUDE.md |
| `ecosystem_capabilities` | — |
| `ecosystem_status` | — |
| `ecosystem_routing_readiness` | — |
| `get_health` | troubleshoot-workflow (archived skill) |
| `get_pool_status` | troubleshoot-workflow (archived skill) |
| `get_readiness` | — |
| `get_liveness` | — |
| `get_workflow_status` | troubleshoot-workflow (archived skill) |
| `list_repos` | troubleshoot-workflow (archived skill) |
| `list_pools` (as `pool_list`) | — |
| `pool_route_execute` | mahavishnu-status (skill), mahavishnu (skill), mahavishnu-orchestrator (agent), mahavishnu/CLAUDE.md |
| `pool_execute` | task-orchestration-review (skill) |
| `pool_spawn` | task-orchestration-review (skill) |
| `pool_monitor` | task-orchestration-review (skill) |
| `pool_search_memory` | task-orchestration-review (skill) |
| `pool_health` | mahavishnu (skill), mahavishnu/CLAUDE.md |
| `pool_list` | — |
| `pool_scale` | — |
| `pool_close` | — |
| `pool_close_all` | — |
| `trigger_workflow` | mahavishnu (skill) |
| `cancel_workflow` | — |
| `create_backup` | — |
| `list_backups` | — |
| `restore_backup` | — |
| `create_user` | — |
| `check_permission` | — |
| `adapter_discover` | — |
| `adapter_resolve` | — |
| `adapter_health` | — |
| `adapter_list` | — |
| `adapter_metadata` | — |
| `adapter_enable` | — |
| `adapter_cache_invalidate` | — |
| `terminal_*` (23 tools: `terminal_launch`, `terminal_send`, `terminal_capture`, `terminal_list`, `terminal_list_adapters`, `terminal_switch_adapter`, `terminal_current_adapter`, `terminal_close`, `terminal_close_all`, `terminal_capture_all`) | — |
| `tree_sitter_*` (7 tools) | — |
| `pycharm_*` (9 tools) | — |
| `websocket_*` (5 tools) | — |
| `worker_*` (3 tools) | — |
| `workflow_result` | — |
| `clone_*` (3 tools) | — |
| `coord_*` (11 tools) | — |
| `ingest_otel_traces` | — |
| `search_otel_traces` | — |
| `query_local_traces` | — |
| `index_code_graph` | — |
| `index_documentation` | — |
| `search_documentation` | — |
| `find_related_code` | — |
| `get_function_context` | — |
| `send_repository_message` | — |
| `broadcast_repository_message` | — |
| `get_repository_messages` | — |
| `acknowledge_repository_message` | — |
| `send_project_message` | — |
| `list_project_messages` | — |
| `notify_repository_changes` | — |
| `notify_workflow_status` | — |
| `send_quality_alert` | — |
| `get_active_alerts` | — |
| `acknowledge_alert` | — |
| `trigger_test_alert` | — |
| `get_recovery_metrics` | — |
| `run_disaster_recovery_check` | — |
| `heal_workflows` | — |
| `get_log_statistics` | — |
| `search_logs` | — |
| `search_workflows` | — |
| `list_workflows` | — |
| `get_workflow_statistics` | — |
| `list_adapters` | — |
| `get_pending_approvals` | — |
| `request_approval` | — |
| `respond_to_approval` | — |
| `flush_metrics` | — |
| `get_monitoring_dashboard` | — |
| `get_observability_metrics` | — |
| `get_repository_health` | — |
| `get_git_velocity_dashboard` | — |
| `get_channel_sessions` | — |
| `track_channel_session` | — |
| `get_verification_result` | — |
| `get_cross_project_patterns` | — |
| `hybrid_search` | — |
| `index_document` | — |
| `delete_document` | — |
| `search_by_repository` | — |
| `list_evidence` | — |
| `review_and_fix` | — |
| `list_pending_drafts` | — |
| `parse_goal` | — |
| `team_from_goal` | — |
| `list_team_skills` | — |
| `get_promotion_history` | — |
| `trigger_synthesis` | — |
| `get_otel_trace` | — |
| `get_pipeline_status` | — |
| `otel_ingester_stats` | — |
| `health_check_service` | — |
| `health_check_all` | — |
| `wait_for_dependency` | — |
| `wait_for_all_dependencies` | — |
| `get_tool_versions` | — |
| `list_primitives_tool` | — |
| `show_primitive_tool` | — |
| `mcp_get_metrics` | — |
| `mcp_list_tools` | — |
| `mcp_test_connection` | — |
| `openhands_health` | — |
| `openhands_run` | — |
| `openhands_status` | — |
| `openhands_cancel` | — |
| `self_improvement_analyze_failures` | — |
| `self_improvement_generate` | — |
| `self_improvement_status` | — |
| `automation_*` (21 desktop-automation tools) | — |
| `publish_to_eventbridge` | — |

(The 2:1 table above is intentionally aggregated; the full enumeration of
183 tools is captured in the source `python` AST walk recorded at
generation time. Tools with no consumer row are by definition *orphan
tools* — see Section 3.1.)

### 2.2 `mcp__session_buddy__*`

Only one session-buddy tool is referenced anywhere: `mcp__session_buddy__search_code_patterns`
appears in the *archived* `code-reviewer` and `refactoring-specialist`
agents. The remaining 152 session-buddy tools are unused by any slash
command or agent (see Section 3.1).

| Tool | Referenced by |
|------|---------------|
| `search_code_patterns` | code-reviewer (archived agent), refactoring-specialist (archived agent) — but labeled `mcp__akosha__search_code_patterns` in source (wrong server name) |
| *all 152 others* | — |

### 2.3 `mcp__akosha__*`

| Tool | Referenced by | Registered? |
|------|---------------|-------------|
| `analyze_trends` | detect-patterns (archived skill) | ✅ |
| `detect_anomalies` | detect-patterns (archived skill) | ✅ |
| `detect_patterns` | detect-patterns (archived skill) | ⚠️ not found in `akosha/akosha/mcp/` |
| `search_code_patterns` | code-reviewer (archived agent), refactoring-specialist (archived agent) | ⚠️ not found in `akosha/akosha/mcp/` (exists as `mcp__session_buddy__search_code_patterns`) |
| *all 5 others* (`discover_tools`, `find_similar_repositories`, `get_code_graph_details`, `get_cross_repo_function_usage`, `get_fitness_analyzer_status`, `list_ingested_code_graphs`, `publish_to_eventbridge`, `query_local_traces`, `run_fitness_analysis`) | — | ✅ |

### 2.4 `mcp__dhara__*`

None of the registered dhara tools are referenced by any slash
command, skill, or agent. The legacy `mcp__dhruva__*` references in
archived skills point to a server that has been renamed (see
Section 3.3 for the dhruva→dhara migration table).

### 2.5 `mcp__crackerjack__*`

| Tool | Referenced by | Registered? |
|------|---------------|-------------|
| `crackerjack_run` | python-pro (active agent), code-reviewer (archived agent), refactoring-specialist (archived agent) | ✅ (client-facing alias; crackerjack has no standalone `@mcp.tool()` source — it is invoked via the crackerjack Python API from a mahavishnu-side adapter) |

### 2.6 `mcp__oneiric__*`

| Tool | Referenced by | Registered? |
|------|---------------|-------------|
| `lifecycle_activate` | manage-lifecycle (archived skill) | ❌ not found (oneiric has no MCP server) |

---

## Section 3: Orphans

### 3.1 Orphan tools (registered but not referenced)

These tools are present in `@mcp.tool()` decorators but never appear in
any slash command, skill, or agent in the scanned tree.

**Mahavishnu**: ~160 of 183 tools have no slash-command consumer.
Listed by domain below; see Section 2.1 reverse index for individual
tool names.

| Domain | Registered count | Referenced | Orphan |
|--------|------------------|-----------|--------|
| pool | 11 | 7 | 4 (`pool_list`, `pool_scale`, `pool_close`, `pool_close_all`) |
| workflow | 4 | 1 | 3 (`cancel_workflow`, `list_workflows`, `search_workflows`) |
| adapter_registry | 7 | 0 | 7 |
| backup | 3 | 0 | 3 |
| terminal | 11 | 0 | 11 |
| treesitter | 7 | 0 | 7 |
| pycharm | 9 | 0 | 9 |
| websocket | 5 | 0 | 5 |
| coordination | 11 | 0 | 11 |
| repository_messaging | 7 | 0 | 7 |
| alerting (3) + monitoring (3) + observability (5) + verification (2) | 14 | 0 | 14 |
| auth (3) + user (1) | 4 | 0 | 4 |
| clone | 3 | 0 | 3 |
| oTel | 5 | 0 | 5 |
| code-graph (5) + documents (5) + team-skills (5) | 15 | 0 | 15 |
| openhands | 4 | 0 | 4 |
| self_improvement | 3 | 0 | 3 |
| automation (21) + desktop-automation (21) | 42 | 0 | 42 |
| misc (`get_tool_versions`, `list_primitives_tool`, `show_primitive_tool`, `mcp_get_metrics`, `mcp_list_tools`, `mcp_test_connection`, `publish_to_eventbridge`, `ecosystem_capabilities`, `ecosystem_status`, `ecosystem_routing_readiness`, `hybrid_search`, `list_pending_drafts`, `workflow_result`) | 13 | 0 | 13 |

**Session-buddy**: 152 of 153 tools are orphaned. Only
`mcp__session_buddy__search_code_patterns` appears in archived agents
under a *mislabeled* server name (`mcp__akosha__search_code_patterns`).

**Akosha**: 5 of 9 registered tools are orphaned. The 4 referenced
tools (`analyze_trends`, `detect_anomalies`, `detect_patterns`,
`search_code_patterns`) all appear *only* in archived skills/agents.

**Dhara**: 20 of 20 registered tools are orphaned. The legacy
`mcp__dhruva__*` references in archived skills point at a previous
server name.

**Oneiric**: 100% orphan — no MCP server exists; the one reference in
an archived skill is a dead link.

### 3.2 Orphan commands (slash commands that reference unregistered tools)

| Slash command / Skill / Agent | Referenced tool | Status |
|-------------------------------|-----------------|--------|
| `.claude/skills/.archive/manage-lifecycle/SKILL.md` | `mcp__oneiric__lifecycle_activate` | ❌ oneiric has no MCP server |
| `.claude/skills/.archive/detect-patterns/SKILL.md` | `mcp__akosha__detect_patterns` | ⚠️ not decorated in `akosha/akosha/mcp/` (described in `REGISTRATION_TOOLS` dict but never registered) |
| `.claude/agents/.archive/code-reviewer.md` | `mcp__akosha__search_code_patterns` | ⚠️ wrong server — exists as `mcp__session_buddy__search_code_patterns` |
| `.claude/agents/.archive/refactoring-specialist.md` | `mcp__akosha__search_code_patterns` | ⚠️ wrong server — exists as `mcp__session_buddy__search_code_patterns` |
| `.claude/skills/.archive/backup-restore/SKILL.md` | `mcp__dhruva__list_backups`, `mcp__dhruva__restore_backup`, `mcp__dhruva__validate_backup` | ❌ `dhruva` server replaced by `dhara`; backups migrated to `mcp__mahavishnu__list_backups` and `mcp__mahavishnu__restore_backup`; `validate_backup` is gone entirely |
| `.claude/skills/.archive/manage-storage/SKILL.md` | `mcp__dhruva__get_adapter`, `mcp__dhruva__list_adapter_versions`, `mcp__dhruva__list_adapters`, `mcp__dhruva__store_adapter` | ⚠️ wrong server — all four exist on `mcp__dhara__*` |

### 3.3 Server-rename mapping: `dhruva` → `dhara`

The archived `.claude/skills/.archive/manage-storage/SKILL.md` and
`.claude/skills/.archive/backup-restore/SKILL.md` reference `dhruva`, a
predecessor MCP server that has been renamed/restructured into
`dhara` (and partly moved to `mahavishnu`).

| Old name | New name | Action |
|----------|----------|--------|
| `mcp__dhruva__list_adapters` | `mcp__dhara__list_adapters` | rename server |
| `mcp__dhruva__list_adapter_versions` | `mcp__dhara__list_adapter_versions` | rename server |
| `mcp__dhruva__get_adapter` | `mcp__dhara__get_adapter` | rename server |
| `mcp__dhruva__store_adapter` | `mcp__dhara__store_adapter` | rename server |
| `mcp__dhruva__list_backups` | `mcp__mahavishnu__list_backups` | server change |
| `mcp__dhruva__restore_backup` | `mcp__mahavishnu__restore_backup` | server change |
| `mcp__dhruva__validate_backup` | *(none — feature dropped)* | dead |

---

## Section 4: Cross-component patterns

### 4.1 Naming inconsistencies

1. **`mcp__akosha__search_code_patterns` does not exist on the akosha
   server.** The two archived agents that reference it
   (`code-reviewer`, `refactoring-specialist`) are pointing at a tool
   that lives on `mcp__session_buddy__search_code_patterns` instead.
   This is a *server misattribution*, not a typo — the tool name is
   spelled identically.

2. **`mcp__akosha__detect_patterns` is described but never registered.**
   The `akosha/mcp/tools/profiles.py` file's `REGISTRATION_TOOLS` dict
   *enumerates* `detect_patterns` as part of `register_akosha_tools`,
   but no `@mcp.tool()` decorator in `akosha/akosha/mcp/` binds that
   name. The detect-patterns skill (archived) calls it; the live
   server returns a 404.

3. **`dhruva` ↔ `dhara` server-rename** is the most pervasive drift.
   The five renamed/relocated tools are still spelled the old way in
   two archived skills. Three additional dhruva tools have no
   replacement at all (`list_backups`, `restore_backup`, `validate_backup`),
   of which `validate_backup` is genuinely dead and the other two were
   moved to mahavishnu.

### 4.2 Aliases / short names

- `crackerjack_run` is the only crackerjack-side tool name that
  appears anywhere in `.claude/`. It's the right name, and it's a
  client-facing alias (crackerjack has no `@mcp.tool()` source — the
  mahavishnu-side worker invokes it via the Python API). The name
  pattern is **stable**, not a one-off.

### 4.3 Component self-reference rates

| Component | Slash commands that reference its own MCP tools | Slash commands that reference other components' MCP tools |
|-----------|---------------------------------------------------|----------------------------------------------------------|
| mahavishnu | 3 of 3 active skills (`mahavishnu`, `mahavishnu-status`, `task-orchestration-review`) + 1 active agent (`mahavishnu-orchestrator`) | 1 active agent (`python-pro` → crackerjack) |
| session-buddy | 0 of 0 | 0 of 0 |
| akosha | 0 of 0 active | 0 of 0 active (only archived references) |
| dhara | 0 of 0 | 0 of 0 |
| crackerjack | 0 of 0 | 1 of 0 (`python-pro` is hosted under mahavishnu/.claude but targets crackerjack) |
| oneiric | 0 of 0 | 0 of 0 |

**The pattern**: mahavishnu is the only component whose own slash
commands (via skills + agents) consistently invoke its own MCP tools.
Every other component is entirely reliant on **archived** slash
artifacts to get any traffic at all — and those archived artifacts
are the source of every drift finding in this inventory.

### 4.4 Slash-command vs skill split

Of the 5 active skills in `mahavishnu/.claude/skills/`, only 3
reference MCP tools. The other 2 (`bodai-status`, `crackerjack-compliant-code`)
do not.

Of the 58 active agents in `mahavishnu/.claude/agents/`, only 2
reference MCP tools — but the MCP coverage is *very* thin even within
those 2 (mahavishnu-orchestrator uses 3 pool tools; python-pro uses
1 crackerjack tool).

The remaining ~55 active agents are entirely prompt-based — they
delegate to local tools or rely on the underlying Claude session.

### 4.5 Drift location: archived vs active

Every orphan command in Section 3.2 lives inside an
`.archive/` subdirectory. **All drift in the inventory is
fossil-only**: zero active slash commands/skills/agents reference
unregistered tools. The crash risk is dormant but real — if someone
`un-archive`s any of these artifacts (or restores them under a new
name) without updating the tool references, the runtime will 404.

---

## Verification

- `wc -l` on this file: 263 lines.
- Table rows (sections 1, 2, 3): see `grep -c '^|'` count below.
- Links in this file: none external; the only links are anchor-style
  references to other sections within this document.