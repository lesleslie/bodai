# PyCharm MCP Integration Plan for Crackerjack

**Status**: Draft for Review
**Created**: 2026-02-24
**Priority**: High
**Estimated Effort**: Medium (2-3 sessions)

______________________________________________________________________

## Executive Summary

Integrate PyCharm's IDE-level diagnostics into Crackerjack's quality checking workflow via MCP. The integration leverages existing infrastructure (`PyCharmMCPAdapter`) and follows established patterns for tool registration.

**Key Insight**: Crackerjack already has a `PyCharmMCPAdapter` with circuit breaker, caching, and fallback mechanisms. The work is ~60% complete - we just need to expose it via MCP tools and integrate with the unified `ToolIssue` model.

______________________________________________________________________

## Current State

### Existing Infrastructure

```
crackerjack/
├── services/
│   └── pycharm_mcp_integration.py    # ✅ EXISTS - Circuit breaker, caching, fallbacks
├── adapters/
│   └── _tool_adapter_base.py         # ✅ EXISTS - ToolIssue dataclass
└── mcp/
    └── tools/
        ├── __init__.py               # Needs update
        └── [various tools]           # Pattern established
```

### PyCharmMCPAdapter Capabilities

| Method | Purpose | Status |
|--------|---------|--------|
| `search_regex()` | Pattern search in codebase | Ready |
| `get_file_problems()` | IDE diagnostics | Ready |
| `replace_text_in_file()` | Text replacement | Ready |
| `reformat_file()` | IDE formatting | Ready |
| `health_check()` | Connection status | Ready |

### ToolIssue Model (Unified)

```python
@dataclass
class ToolIssue:
    file_path: Path
    line_number: int | None = None
    column_number: int | None = None
    message: str = ""
    code: str | None = None
    severity: str = "error"  # error, warning, info
    suggestion: str | None = None
```

______________________________________________________________________

## Implementation Plan

### Phase 1: MCP Tool Exposure (Primary)

Create `/crackerjack/mcp/tools/pycharm_tools.py`:

```python
"""PyCharm MCP Tools for IDE-level diagnostics and operations."""

import json
import typing as t
from pathlib import Path

from crackerjack.mcp.context import get_context
from crackerjack.services.pycharm_mcp_integration import PyCharmMCPAdapter


def register_pycharm_tools(mcp_app: t.Any) -> None:
    """Register PyCharm integration tools with the MCP server."""
    _register_get_ide_diagnostics_tool(mcp_app)
    _register_search_code_tool(mcp_app)
    _register_get_symbol_info_tool(mcp_app)
    _register_pycharm_health_tool(mcp_app)


def _get_adapter() -> PyCharmMCPAdapter:
    """Get or create the PyCharm MCP adapter."""
    context = get_context()
    # Adapter singleton stored in context
    if not hasattr(context, "pycharm_adapter"):
        context.pycharm_adapter = PyCharmMCPAdapter(
            mcp_client=None,  # Will use MCP tools directly
            timeout=30.0,
            max_results=100,
        )
    return context.pycharm_adapter


def _register_get_ide_diagnostics_tool(mcp_app: t.Any) -> None:
    @mcp_app.tool()
    async def get_ide_diagnostics(
        file_path: str,
        errors_only: bool = False,
        include_inspections: bool = True,
    ) -> str:
        """Get IDE-level diagnostics for a file from PyCharm.

        Args:
            file_path: Path to the file to analyze
            errors_only: If True, only return errors (not warnings)
            include_inspections: If True, include code inspection results

        Returns:
            JSON string with list of diagnostic issues
        """
        adapter = _get_adapter()
        problems = await adapter.get_file_problems(file_path, errors_only)

        # Convert to ToolIssue format for consistency
        issues = []
        for problem in problems:
            issues.append({
                "file_path": file_path,
                "line_number": problem.get("line"),
                "column_number": problem.get("column"),
                "message": problem.get("message", ""),
                "code": problem.get("code"),
                "severity": problem.get("severity", "warning"),
                "suggestion": problem.get("quick_fix"),
                "source": "pycharm",
            })

        return json.dumps({
            "success": True,
            "issues": issues,
            "count": len(issues),
        })


def _register_search_code_tool(mcp_app: t.Any) -> None:
    @mcp_app.tool()
    async def search_code(
        pattern: str,
        file_pattern: str | None = None,
    ) -> str:
        """Search for a regex pattern in the codebase via PyCharm index.

        Args:
            pattern: Regex pattern to search for
            file_pattern: Optional glob pattern to filter files (e.g., "*.py")

        Returns:
            JSON string with search results
        """
        adapter = _get_adapter()
        results = await adapter.search_regex(pattern, file_pattern)

        return json.dumps({
            "success": True,
            "results": [
                {
                    "file_path": r.file_path,
                    "line": r.line_number,
                    "column": r.column,
                    "match": r.match_text,
                    "context_before": r.context_before,
                    "context_after": r.context_after,
                }
                for r in results
            ],
            "count": len(results),
        })


def _register_get_symbol_info_tool(mcp_app: t.Any) -> None:
    @mcp_app.tool()
    async def get_symbol_info(symbol_name: str) -> str:
        """Get information about a code symbol from PyCharm's index.

        Args:
            symbol_name: Name of the symbol to look up

        Returns:
            JSON string with symbol information (type, usages, definition)
        """
        # This would call PyCharm MCP's get_symbol_info tool
        # Placeholder for now - requires PyCharm MCP server connection
        return json.dumps({
            "success": False,
            "error": "PyCharm MCP connection not yet configured",
            "symbol": symbol_name,
        })


def _register_pycharm_health_tool(mcp_app: t.Any) -> None:
    @mcp_app.tool()
    async def pycharm_health() -> str:
        """Check the health of the PyCharm MCP connection.

        Returns:
            JSON string with connection status and metrics
        """
        adapter = _get_adapter()
        health = await adapter.health_check()

        return json.dumps({
            "success": True,
            **health,
        })
```

### Phase 2: Tool Registration

Update `/crackerjack/mcp/tools/__init__.py`:

```python
# Add import
from .pycharm_tools import register_pycharm_tools

# Add to __all__
__all__ = [
    # ... existing ...
    "register_pycharm_tools",
]
```

Update `/crackerjack/mcp/server_core.py`:

```python
# Add import
from .tools import (
    # ... existing ...
    register_pycharm_tools,
)

# In create_mcp_server() function, add:
register_pycharm_tools(mcp_app)
```

### Phase 3: Diagnostic Adapter (Optional Enhancement)

Create `/crackerjack/adapters/ide/pycharm.py` for unified diagnostic integration:

```python
"""PyCharm diagnostic adapter following the tool adapter pattern."""

from dataclasses import dataclass
from pathlib import Path

from crackerjack.adapters._tool_adapter_base import BaseToolAdapter, ToolIssue


class PyCharmDiagnosticAdapter(BaseToolAdapter):
    """Adapter for PyCharm IDE diagnostics."""

    def __init__(self, pycharm_adapter: t.Any) -> None:
        self._adapter = pycharm_adapter

    async def check_file(self, file_path: Path) -> list[ToolIssue]:
        """Check a file and return issues in ToolIssue format."""
        problems = await self._adapter.get_file_problems(str(file_path))

        return [
            ToolIssue(
                file_path=file_path,
                line_number=p.get("line"),
                column_number=p.get("column"),
                message=p.get("message", ""),
                code=p.get("code"),
                severity=self._map_severity(p.get("severity", "warning")),
                suggestion=p.get("quick_fix"),
            )
            for p in problems
        ]

    def _map_severity(self, pycharm_severity: str) -> str:
        """Map PyCharm severity to Crackerjack severity."""
        mapping = {
            "ERROR": "error",
            "WARNING": "warning",
            "WEAK_WARNING": "info",
            "INFO": "info",
            "TYPO": "info",
        }
        return mapping.get(pycharm_severity.upper(), "warning")
```

______________________________________________________________________

## MCP Tools Summary

| Tool | Purpose | PyCharm MCP Dependency |
|------|---------|------------------------|
| `get_ide_diagnostics` | Get IDE-level diagnostics | `get_file_problems` |
| `search_code` | Search codebase via index | `search_regex` |
| `get_symbol_info` | Symbol lookup | `get_symbol_info` |
| `pycharm_health` | Connection status | `health_check` |

______________________________________________________________________

## Configuration

Add to `pyproject.toml`:

```toml
[tool.crackerjack.pycharm]
enabled = true
# MCP server connection (if remote)
mcp_url = "http://localhost:8676"
# Timeouts
timeout_seconds = 30
# Cache settings
diagnostics_cache_ttl = 10
search_cache_ttl = 60
# Circuit breaker
failure_threshold = 3
recovery_timeout = 60
```

______________________________________________________________________

## Testing Strategy

### Unit Tests

```python
# tests/mcp/tools/test_pycharm_tools.py

import pytest
from unittest.mock import AsyncMock, patch

pytestmark = pytest.mark.anyio


async def test_get_ide_diagnostics_returns_issues():
    """Test that get_ide_diagnostics returns properly formatted issues."""
    with patch("crackerjack.mcp.tools.pycharm_tools._get_adapter") as mock:
        adapter = AsyncMock()
        adapter.get_file_problems.return_value = [
            {"line": 10, "column": 5, "message": "Unused import", "severity": "WARNING"}
        ]
        mock.return_value = adapter

        # Call the tool
        result = await get_ide_diagnostics("test.py")
        data = json.loads(result)

        assert data["success"] is True
        assert data["count"] == 1
        assert data["issues"][0]["line_number"] == 10


async def test_circuit_breaker_opens_on_failures():
    """Test that circuit breaker opens after threshold failures."""
    adapter = PyCharmMCPAdapter(mcp_client=None)

    # Simulate failures
    for _ in range(3):
        adapter._circuit_breaker.record_failure()

    assert adapter._circuit_breaker.is_open is True
```

### Integration Tests

```python
# tests/integration/test_pycharm_integration.py

async def test_full_diagnostic_workflow():
    """Test the complete diagnostic workflow with PyCharm."""
    # This test requires PyCharm MCP server running
    result = await mcp_client.call_tool("get_ide_diagnostics", {
        "file_path": "crackerjack/services/pycharm_mcp_integration.py"
    })

    assert result["success"] is True
    # Should find at least some diagnostics in a real file
```

______________________________________________________________________

## Dependencies

### Required (Already Present)

- `fastmcp` - MCP framework
- `mcp-common` - Shared utilities
- PyCharm MCP server (running)

### Optional Enhancements

- `pycharm-mcp-client` - Direct PyCharm connection (future)

______________________________________________________________________

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| PyCharm MCP not available | Medium | Low | Fallback to CLI tools |
| Performance degradation | Low | Medium | Circuit breaker + caching |
| Version incompatibility | Low | Medium | Version check in health |

______________________________________________________________________

## Success Criteria

1. **MCP Tools Registered**: All 4 tools visible in MCP tool list
1. **Diagnostics Retrieved**: `get_ide_diagnostics` returns issues from PyCharm
1. **Circuit Breaker Works**: Failures don't cascade
1. **Cache Works**: Repeated calls are fast
1. **Fallback Works**: Works without PyCharm connection

______________________________________________________________________

## Timeline

| Phase | Tasks | Session |
|-------|-------|---------|
| 1 | Create pycharm_tools.py, register tools | 1 |
| 2 | Integration testing | 1-2 |
| 3 | Diagnostic adapter (optional) | 2-3 |
| 4 | Documentation and polish | 3 |

______________________________________________________________________

## Next Steps

1. **Review this plan** - Confirm approach and priorities
1. **Create pycharm_tools.py** - Implement Phase 1
1. **Test with real PyCharm** - Verify MCP connection works
1. **Iterate** - Add diagnostic adapter if needed

______________________________________________________________________

## Related Documents

- [Bodai Architecture](architecture.md)
- Crackerjack PyCharm MCP Integration Service (in `crackerjack/crackerjack/services/pycharm_mcp_integration.py`)
- Crackerjack Tool Adapter Base (in `crackerjack/crackerjack/adapters/_tool_adapter_base.py`)
